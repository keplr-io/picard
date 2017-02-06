# Picard: Declarative hyperparameter experiments for neural networks

Picard lets you easily declare large spaces of ([keras](https://keras.io/)) neural networks and to run ([hyperopt](http://hyperopt.github.io/hyperopt/) optimization experiments on them.

Here's a quick [tutorial](http://picard.libs.keplr.io/tutorial)

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Model Building](#model-building)
    - [Overview](#overview)
    - [Operators](#operators)
    - [Legs](#legs)
    - [Edges](#edges)
    - [Fit](#fit)
    - [Data](#data)
- [Hyperparameter Operations](#hyperparameter-operations)


## Installation

Install right from the repo with pip & git+https
```bash
    pip install git+https://github.com/jakebian/picard.git

```

## Basic Usage

```py

from picard.minimizer import get_min_model
from picard.util.data import get_picard_input
from hyperopt import Trials
import numpy as np

min_model = get_min_model(
    spec= {
        ...
    },
    data=get_picard_input(
        dataspec, {
            'myInputFieldName': np.loadtxt('./datain.csv'),
            'myOutputFieldName': np.loadtxt('./dataout.csv')
        }
    ),
    trials=Trials(),
    max_evals=15
)

```


**Word of warning**

The objective function of the hyperparameter optimization is the loss on the testing set. Of course it is possible to overfit in this "meta-learning" procedure - hence it's advisable to set apart a meta-testing set to test your model against when using Picard.

## Hyperparameter Operations

Hyperparameter operations in Picard gives you access to any operation in Hyperopt. Combined with the model syntax (explained below) above this gives you powerful ways to quickly build complex spaces of model hyperparameters.

You can desinate any value in a picard configuration to be a hyperparameter by replacing it with a hyperparameter spec. Some examples:

- Tune the probability `p` in my dropout layer (operator) between 0.1 and 0.5

```js
{
    "operators": {
        "denseLayer": {
            "layer": "Dense",
            "config": {
                "p": {
                    "&uniform": {
                        "low": 0.1,
                        "high": 0.5
                    }
                }
            }
        },
        ...
    },
    ...
}
```

- Use between 3 and 6 dense layers in succession

```js
{
    "operators": {
        "feedForward": {
            "#repeat": {
                "operator": "denseLayer",
                "+times": {
                    "&choice": [3, 4, 5, 6]
                }
            }
        }
    }
}
```


There are also picard operators that generate hyperopt specs from model specs. For example:

- Decide whether to add a dropout layer
```js
{
    "operators": {
        "#compose": [
            "feedForward": {...},
            {
                "#optional": {
                    "layer": "Dropout",
                    "config": {
                        "p": {
                            "&uniform": {
                              "high": 0.3,
                              "low": 0.1
                            }
                        }
                    }
                }
            }
        ]
    }
}
```



Note these are not limited to numerical values, and that they apply not only to the operator spec. Here's an example of using `#optional` to decide whether to add an edge in the model graph

```js
{
    "edges": {
        ...,
        {
            "#optional": {
                "operator": 'op1',
                "source": 's1',
                "target": 't1'
            }
        },
        ...
    }
}
```




## Model Building

### Overview

The format for a picard configuration looks something like this

At a high level:

- The `space` field specifies what kind of model you want to build and how you want to train it
- The `data` field specify how to feed your dataset into your model. For example, how to assign columns in your dataset to legs in the model graph.

```js
    {

        "space": {
            "operators": {
                <operatorKey>: {<operatorSpec>},
                ...
            },
            "legs": {
                "in": {
                    <inputLegKey>: <inputLayerSpec>,
                    ...
                },
                "out": {
                    <outputLegKey>: <outputLegSpec>,
                    ...
                }
            },
            "edges": [
                {
                    "operator": <operatorKey>,
                    "source": <sourceNodeKey>,
                    "target": <targetNodeKey>
                },
                ...
            ],
            "fit": {<Keras training options>}
        },

        "data": {
            "fields": {
                /* metadata for fields/columns in your dataset */
                <fieldKey>: {
                    "shape": [<dimensions of your input>]
                }
            },
            "in": [
                /* how to assign data fields to input legs */
                {
                    "field": <fieldKey>,
                    "leg": <legKey>
                },
                ...
            ],
            "out": [
                /* how to assign data fields to output legs */
                {
                    "field": <fieldKey>,
                    "leg": <legKey>
                },
                ...
            ],
            "training": {
                /* options for training */
                "epochs": <how many epochs to train>
                "val_split": <validation split during training> // float between 0 and 1
                "split": <training/testing split>  // float between 0 and 1
            }
        }

    }
```


### Operators

Operators layers and compositions of layers in the neural network.

**Simple Keras Operators**

Any layer in Keras is available as an operator in Picard

```js
{
    ...
    "operators": {
        <operatorKey>: {
            "layer": <keras layer name>,
            "config": <oprtions for keras layer>
        }
    }
}
```

For example:

```js
{
    "myDropoutOperator": {
        "layer": "Dropout",
        "config": {
            "p": 0.1
        }
    }
}
```

**Composite Operators**

Picard supports several convenient ways to specify how to stack layers togetheer.

**#compose**

`#compose` defines an operator via a sequence operator specs

```js
{
    <operatorKey>: {
        "#compose": [
            <operatorSpec1>,
            <operatorSpec2>,
            ...
        ]
    }
}
```

For example:

```js
{
    "denseThenDropout": {
        "#compose": [
            {
              "layer": "Dense",
              "config": {
                "output_dim": 512,
                "activation": "relu"
              }
            },
            {
                "layer": "Dropout",
                "config": {
                  "p": 0.1
                }
            }
        ]
    }
}
```

**#repeat**

`#repeat` is a shorthand for the `#comopose` operation that just tells you to compose a layer with itself some number of times

```js
{
    <operatorKey>: {
        "#repeat": {
            "operator": <operatorSpec>,
            "times": <number of times to compose the operator with itself>
        }
    }
}
```


For example
```js
{
    "simpleFeedForwardStack": {
        "#repeat": {
            "operator": {
                "layer": "Dense",
                "config": {
                    "output_dim": 512,
                    "activation": "relu"
                }
            },
            "times": 5
        }
    }
}
```


**Built-in special operators**

- The "IDENTITY" operator is an operator that act as the identity on a tensor.


### Legs

The `legs` field generates `Input` and `Output` layers in Keras

```js
{
    "legs": {
        "in": {
            <inputLegKey>: <inputLayerSpec>,
            ...
        },
        "out": {
            <outputLegKey>: <outputLegSpec>,
            ...
        }
    }
}
```

where `inputLayerSpec`, `outputLegSpec` are respectively options for the keras Input and Output layers.

### Edges

The `edges` field specifies the model graph

```js
{
    ...,
    "edges": [
        {
            "operator": <operatorKey>,
            "source": <sourceNodeKey>,
            "target": <targetNodeKey>
        },
        ...
    ],
}
```

where a nodeKey is one of

- the key of an input or output leg
- some arbitrary string identifying an endpoint of the edge in the model graph


For example, here's the edges spec for a model that goes through 2 dense layers then a dropout

```js
{
    "edges": [
        {
            "operator": "IDENTITY",
            "source": "input",
            "target": "dense-start"
        },
        {
            "operator": "ff",
            "source": "dense-start",
            "target": "dense-end"
        },
        {
            "operator": "dropout",
            "source": "dense-end",
            "target": "output"
        }
    ],
    "operators": {
        "ff": {
            "#repeat": {
                "operator": {
                    "layer": "dense",
                    "config": {...}
                },
                "times": 2
            }
        },
        "dropout": {
            "layer": "Dropout",
            "config": { ... }
        }
    }
    "legs": {
        "in": {
            "input": {...},
        },
        "out": {
            "output": {...}
        }
    },
}
```

### Fit
The `fit` field is any configuration for `model.fit` in keras:

```js
{
    ...,
    "fit": {
      "batch_size": 32
    },
}
```

### Data


```js
{
    "fields": {
        /* metadata for fields/columns in your dataset */
        <fieldKey>: {
            "shape": [<dimensions of your input>]
        }
    },
    "in": [
        /* how to assign data fields to input legs */
        {
            "field": <fieldKey>,
            "leg": <legKey>
        },
        ...
    ],
    "out": [
        /* how to assign data fields to output legs */
        {
            "field": <fieldKey>,
            "leg": <legKey>
        },
        ...
    ],
    "training": {
        /* options for training */
        "epochs": <how many epochs to train>
        "val_split": <validation split during training> // float between 0 and 1
        "split": <training/testing split>  // float between 0 and 1
    }
}
```


