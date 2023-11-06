from modules.VTS.model import Model, Models
from modules.VTS.expression import Expression, Expressions
from modules.VTS.coords import Coords
from modules.VTS.position import Position, Model_Position, Model_Positions
from modules.shared import report_error
import json

VTS_MODELS = Models()
VTS_EXPRESSIONS = Expressions()
VTS_COORDS = Coords()
VTS_MODEL_POSITIONS = Model_Positions()


# functions to manipulate and save objects

'''
json save file format:
array of models object with model name, model id and position object
[
    {
        "name": "model_name1",
        "id": "model_id1",
        "positions": [
            {
                "name": "position1",
                "timeInSeconds": "100",
                "valuesAreRelativeToModel": "relative",
                "positionX": "x1",
                "positionY": "y1",
                "rotation": "rotation1",
                "size": "size1"
            },
            {
                "name": "position2",
                "timeInSeconds": "200",
                "valuesAreRelativeToModel": "relative",
                "positionX": "x2",
                "positionY": "y2",
                "rotation": "rotation2",
                "size": "size2"
            }
        ]
    },
    {
        "name": "model_name2",
        "id": "model_id2",
        "positions": [
            {
                "name": "position3",
                "timeInSeconds": "300",
                "valuesAreRelativeToModel": "relative",
                "positionX": "x3",
                "positionY": "y3",
                "rotation": "rotation3",
                "size": "size3"
            },
            {
                "name": "position4",
                "timeInSeconds": "400",
                "valuesAreRelativeToModel": "relative",
                "positionX": "x4",
                "positionY": "y4",
                "rotation": "rotation4",
                "size": "size4"
            }
        ]
    }
]

'''
# path: /home/izitto/Desktop/Code/PAtDS/variables/VTS_saved_positions.json
saved_positions_Path = "/home/izitto/Desktop/Code/PAtDS/variables/VTS_saved_positions.json"
# function to load json data from file to object VTS_MODEL_POSITIONS
def load_VTS_MODEL_POSITIONS():
    global VTS_MODEL_POSITIONS
    try:
        with open(saved_positions_Path, 'r') as f:
            data = json.load(f)
            VTS_MODEL_POSITIONS.addModel_Positions([Model_Position(model["name"], model["id"], [Position(position["name"], position["timeInSeconds"], position["valuesAreRelativeToModel"], position["positionX"], position["positionY"], position["rotation"], position["size"]) for position in model["positions"]]) for model in data["Model_Positions"]])
    except Exception as e:
        report_error(e)

# function to save object VTS_MODEL_POSITIONS to json file
def save_VTS_MODEL_POSITIONS():
    global VTS_MODEL_POSITIONS
    try:
        with open(saved_positions_Path, 'w') as f:
            json.dump(VTS_MODEL_POSITIONS.toJSON(), f, indent=4)
    except Exception as e:
        report_error(e)

load_VTS_MODEL_POSITIONS()