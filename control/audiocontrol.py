import pyaudio
import json


def get_device_info(p):
    info = {}
    count = p.get_device_count()
    for i in range(count):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            info[i] = {
                'name': device_info['name'],
                'sample_rates': [device_info['defaultSampleRate']]
            }
    return info


def select_device(info):
    print("Available Devices:")
    for index, name in info.items():
        print(f"{index}: {name}")

    while True:
        selection = input("Enter the index of the device you want to select: ")
        if selection.isdigit() and int(selection) in info:
            return int(selection)
        print("Invalid selection. Please try again.")


def save_device_info(mic_name, speaker_name):
    data = {
        'mic': mic_name,
        'speaker': speaker_name
    }
    with open('selected_devices.json', 'w') as f:
        json.dump(data, f)


def load_device_info():
    try:
        with open('selected_devices.json', 'r') as f:
            data = json.load(f)
            return data['mic'], data['speaker']
    except FileNotFoundError:
        return None, None
    except json.decoder.JSONDecodeError:
        return None, None


def main():
    p = pyaudio.PyAudio()
    mic_info = get_device_info(p)
    speaker_info = get_device_info(p)
    saved_mic, saved_speaker = load_device_info()
    if saved_mic and saved_speaker:
        print(
            f"Using saved devices: Mic - {saved_mic}, Speaker - {saved_speaker}")
        mic_index = saved_mic
        speaker_index = saved_speaker
    else:
        print("Select a USB microphone:")
        mic_index = select_device(mic_info)

        print("\nSelect a USB speaker:")
        speaker_index = select_device(speaker_info)

        save_device_info(mic_index, speaker_index)

    # Find the highest supported sample rate for the microphone
    mic_sample_rates = mic_info[mic_index]['sample_rates']
    max_mic_sample_rate = max(mic_sample_rates)

    # Find the highest supported sample rate for the speaker
    speaker_sample_rates = speaker_info[speaker_index]['sample_rates']
    max_speaker_sample_rate = max(speaker_sample_rates)

    # Select the sample rate for the microphone
    mic_sample_rate = max_mic_sample_rate

    # Select the sample rate for the speaker
    speaker_sample_rate = max_speaker_sample_rate

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(mic_sample_rate),
                    frames_per_buffer=4096,
                    input=True,
                    input_device_index=mic_index,
                    output=True,
                    output_device_index=speaker_index)

    print("Streaming audio... Press Ctrl+C to stop.")
    try:
        while True:
            data = stream.read(1024)
            stream.write(data)
    except KeyboardInterrupt:
        print("Stopping...")
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main()
