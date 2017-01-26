hyperspec = {
    'operators': {
        'embedding': {
            'layer': 'Embedding',

            'config': {
                'output_dim': 512,
                'input_dim': 10000,
                'input_length': 500,
                'dropout': 0.2
            }
        },

        'lstm': {
            'layer': 'LSTM',
            'config': {
                'output_dim': 32
            }
        },
        'ff': {
            '#repeat': {
                '+times': {
                    '&choice': {
                        'options': [
                            2,
                            3,
                            4,
                            5
                        ]
                    }
                },
                'operator': {
                    '#compose': [
                        {
                            'layer': 'Dense',
                            'config': {
                                'output_dim': 512,
                                'activation': {
                                    '&choice': {
                                        'options': ['relu', 'sigmoid']
                                    }
                                }
                            }
                        },
                        {
                            '#optional': {
                                'layer': 'Dropout',
                                'config': {
                                    'p': {
                                        '&uniform': {
                                            'low': .1,
                                            'high': .3
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        },
        'denseOut': {
            'layer': 'Dense',
            'config': {
                'output_dim': 1,
                'activation': {
                    '&choice': {
                        'options': ['relu', 'sigmoid', 'softmax']
                    }
                }
            }
        }
    },

    'legs': {
        'in': {'input': {}},
        'out': {'output': {
            'loss': 'binary_crossentropy'
        }}
    },

    'edges': [
        {
            'source': 'input',
            'target': 'emb',
            'operator': 'embedding'
        },
        {
            'source': 'emb',
            'target': 'ffStart',
            'operator': 'lstm'
        },
        {
            'source': 'ffStart',
            'target': 'ffEnd',
            'operator': 'ff'
        },
        {
            'source': 'ffEnd',
            'target': 'output',
            'operator': 'denseOut'
        }
    ],

    'compile': {
        'optimizer': {
            '&choice': {
                'options': ['rmsprop', 'adam']
            }
        }
    },

    'fit': {
        'batch_size': {
            '&choice': {
                'options': [16, 32]
            }
        },
    }
}


expected_result = {
    'compile': {
        'optimizer': {
            '&choice': {
                'options': ['rmsprop', 'adam']
            }
        }
    },
    'operators': {
        'lstm': {
            'layer': 'LSTM',
            'config': {
                'output_dim': 32
            }
        },
        'embedding': {
            'layer': 'Embedding',
            'config': {
                'output_dim': 512,
                'dropout': 0.2,
                'input_dim': 10000,
                'input_length': 500
            }
        },
        'ff': {
            '&choice': {
                'options': [{
                    '#compose': [{
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }, {
                    '#compose': [{
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }, {
                    '#compose': [{
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }, {
                    '#compose': [{
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }, {
                        '&choice': {
                            'options': [{
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }, {
                                    'layer': 'Dropout',
                                    'config': {
                                        'p': {
                                            '&uniform': {
                                                'high': 0.3,
                                                'low': 0.1
                                            }
                                        }
                                    }
                                }]
                            }, {
                                '#compose': [{
                                    'layer': 'Dense',
                                    'config': {
                                        'output_dim': 512,
                                        'activation': {
                                            '&choice': {
                                                'options': ['relu', 'sigmoid']
                                            }
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }]
            }
        },
        'denseOut': {
            'layer': 'Dense',
            'config': {
                'output_dim': 1,
                'activation': {
                    '&choice': {
                        'options': ['relu', 'sigmoid', 'softmax']
                    }
                }
            }
        }
    },
    'legs': {
        'in': {
            'input': {}
        },
        'out': {
            'output': {
                'loss': 'binary_crossentropy'
            }
        }
    },
    'fit': {
        'batch_size': {
            '&choice': {
                'options': [16, 32]
            }
        }
    },
    'edges': [{
        'operator': 'embedding',
        'source': 'input',
        'target': 'emb'
    }, {
        'operator': 'lstm',
        'source': 'emb',
        'target': 'ffStart'
    }, {
        'operator': 'ff',
        'source': 'ffStart',
        'target': 'ffEnd'
    }, {
        'operator': 'denseOut',
        'source': 'ffEnd',
        'target': 'output'
    }]
}