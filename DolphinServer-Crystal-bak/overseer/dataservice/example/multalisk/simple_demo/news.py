# -*- coding: utf-8 -*-
"""
    Simple demo for multalisk
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Http Request:
        http://x.x.x.x:5000/multalisk/report/news001?q={}

"""

import multalisk
from multalisk.model import orm
from multalisk.core.feature import ChartType
from multalisk.utils.custom_filter import n_days_ago


DEBUG = True
APP_CONF = {
    'model': [
        {"model_id": "1001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "1006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "2006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "3006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4001", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4002", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4003", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4004", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4005", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
        {"model_id": "4006", "db_conn":
            "mysql://root:P@55word@127.0.0.1:3306/news_report?charset=utf8"},
    ],
    'view': {
        'total_click_tr_tr': {
            'charts': [
                {
                    'model_id': '1002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'total_click_ru_ru': {
            'charts': [
                {
                    'model_id': '2002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'total_click_ja_jp': {
            'charts': [
                {
                    'model_id': '3002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'total_click_ar_sa': {
            'charts': [
                {
                    'model_id': '4002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        },
        'click_type_ratio_tr_tr': {
            'charts': [
                {
                    'model_id': '1002',
                    'x_dimension': 'type',
                    'y_dimension': [
                        {
                            "name": "click_type_ratio",
                            "value": {
                                "field": "click",
                                "func": "sum_ratio"
                            }},
                    ],
                    'default_q': {"filters": [{
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '1002',
                    'name': 'type',
                }]
            }
        }, 'click_type_ratio_ru_ru': {
            'charts': [
                {
                    'model_id': '2002',
                    'x_dimension': 'type',
                    'y_dimension': [
                        {
                            "name": "click_type_ratio",
                            "value": {
                                "field": "click",
                                "func": "sum_ratio"
                            }},
                    ],
                    'default_q': {"filters": [{
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '2002',
                    'name': 'type',
                }]
            }
        }, 'click_type_ratio_ja_jp': {
            'charts': [
                {
                    'model_id': '3002',
                    'x_dimension': 'type',
                    'y_dimension': [
                        {
                            "name": "click_type_ratio",
                            "value": {
                                "field": "click",
                                "func": "sum_ratio"
                            }},
                    ],
                    'default_q': {"filters": [{
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '3002',
                    'name': 'type',
                }]
            }
        }, 'click_type_ratio_ar_sa': {
            'charts': [
                {
                    'model_id': '4002',
                    'x_dimension': 'type',
                    'y_dimension': [
                        {
                            "name": "click_type_ratio",
                            "value": {
                                "field": "click",
                                "func": "sum_ratio"
                            }},
                    ],
                    'default_q': {"filters": [{
                        'name': 'type',
                        'op': '!=',
                        'val': 'recommend'
                    }, {
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }]},
                    'chart_type': ChartType.Pie
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '4002',
                    'name': 'type',
                }]
            }
        }, 'recommend_click_tr_tr': {
            'charts': [
                {
                    'model_id': '1002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '==',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'recommend_click_ru_ru': {
            'charts': [
                {
                    'model_id': '2002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '==',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'recommend_click_ja_jp': {
            'charts': [
                {
                    'model_id': '3002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '==',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        }, 'recommend_click_ar_sa': {
            'charts': [
                {
                    'model_id': '4002',
                    'x_dimension': 'date',
                    'y_dimension': [
                        {
                            "name": "total_click",
                            "value": {
                                "field": "click",
                                "func": "sum"
                            }
                        }
                    ],
                    'default_q': {"filters": [{
                        'name': 'date',
                        'op': '>=',
                        'val': (n_days_ago, [15, '%Y-%m-%d'])
                    }, {
                        'name': 'type',
                        'op': '==',
                        'val': 'recommend'
                    }]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {}
        },
        'recommend_ratio_tr_tr': {
            'charts': [
                {
                    'model_id': '1004',
                    'x_dimension': 'priority',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '1003',
                    'x_dimension': 'category',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '1005',
                    'x_dimension': 'source',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }],
            'filters': {
                'multi': [{
                    'model_id': '1004',
                    'name': 'priority',
                }, {
                    'model_id': '1003',
                    'name': 'category',
                }, {
                    'model_id': '1005',
                    'name': 'source',
                }]
            }
        }, 'recommend_ratio_ru_ru': {
            'charts': [
                {
                    'model_id': '2004',
                    'x_dimension': 'priority',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '2003',
                    'x_dimension': 'category',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '2005',
                    'x_dimension': 'source',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }],
            'filters': {
                'multi': [{
                    'model_id': '2004',
                    'name': 'priority',
                }, {
                    'model_id': '2003',
                    'name': 'category',
                }, {
                    'model_id': '2005',
                    'name': 'source',
                }]
            }
        }, 'recommend_ratio_ja_jp': {
            'charts': [
                {
                    'model_id': '3004',
                    'x_dimension': 'priority',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '3003',
                    'x_dimension': 'category',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '3005',
                    'x_dimension': 'source',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }],
            'filters': {
                'multi': [{
                    'model_id': '3004',
                    'name': 'priority',
                }, {
                    'model_id': '3003',
                    'name': 'category',
                }, {
                    'model_id': '3005',
                    'name': 'source',
                }]
            }
        }, 'recommend_ratio_ar_sa': {
            'charts': [
                {
                    'model_id': '4004',
                    'x_dimension': 'priority',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '4003',
                    'x_dimension': 'category',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }, {
                    'model_id': '4005',
                    'x_dimension': 'source',
                    'y_dimension': [{
                        'name': 'total_click',
                        'value': {
                            'field': 'recommend_click',
                            'func': 'sum_ratio'
                        }
                    }],
                    'default_q': {'filters': [{
                        'name': 'date',
                        'op': '==',
                        'val': (n_days_ago, [1, '%Y-%m-%d'])
                    }
                    ]},
                    'chart_type': ChartType.Pie
                }],
            'filters': {
                'multi': [{
                    'model_id': '4004',
                    'name': 'priority',
                }, {
                    'model_id': '4003',
                    'name': 'category',
                }, {
                    'model_id': '4005',
                    'name': 'source',
                }]
            }
        },
        'category_click_tr_tr': {
            'charts': [
                {
                    'model_id': '1003',
                    'x_dimension': 'date',
                    'y_dimension': [{
                                "name": "total_click",
                                "value": {
                                    "field_group": 'top_click+home_click+push_click',
                                    "func": "sum"
                                }},
                    ],
                    'default_q': {"filters": [
                        {
                            'name': 'date',
                            'op': '>=',
                            'val': (n_days_ago, [15, '%Y-%m-%d'])
                        },
                        {'name': 'category', 'op': '==', 'val': 1}
                    ]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '1003',
                    'name': 'category',
                }]
            }
        }, 'category_click_ru_ru': {
            'charts': [
                {
                    'model_id': '2003',
                    'x_dimension': 'date',
                    'y_dimension': [{
                                "name": "total_click",
                                "value": {
                                    "field_group": 'top_click+home_click+push_click',
                                    "func": "sum"
                                }},
                    ],
                    'default_q': {"filters": [
                        {
                            'name': 'date',
                            'op': '>=',
                            'val': (n_days_ago, [15, '%Y-%m-%d'])
                        },
                        {'name': 'category', 'op': '==', 'val': 1}
                    ]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '2003',
                    'name': 'category',
                }]
            }
        }, 'category_click_ja_jp': {
            'charts': [
                {
                    'model_id': '3003',
                    'x_dimension': 'date',
                    'y_dimension': [{
                                "name": "total_click",
                                "value": {
                                    "field_group": 'top_click+home_click+push_click',
                                    "func": "sum"
                                }},
                    ],
                    'default_q': {"filters": [
                        {
                            'name': 'date',
                            'op': '>=',
                            'val': (n_days_ago, [15, '%Y-%m-%d'])
                        },
                        {'name': 'category', 'op': '==', 'val': 1}
                    ]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '3003',
                    'name': 'category',
                }]
            }
        }, 'category_click_ar_sa': {
            'charts': [
                {
                    'model_id': '4003',
                    'x_dimension': 'date',
                    'y_dimension': [{
                                "name": "total_click",
                                "value": {
                                    "field_group": 'top_click+home_click+push_click',
                                    "func": "sum"
                                }},
                    ],
                    'default_q': {"filters": [
                        {
                            'name': 'date',
                            'op': '>=',
                            'val': (n_days_ago, [15, '%Y-%m-%d'])
                        },
                        {'name': 'category', 'op': '==', 'val': 1}
                    ]},
                    'chart_type': ChartType.Line
                }
            ],
            'filters': {
                'multi': [{
                    'model_id': '4003',
                    'name': 'category',
                }]
            }
        }, 'category_source_ratio_tr_tr': {
            'charts': [{
                'model_id': '1005',
                'x_dimension': 'source',
                'y_dimension': [{
                    'name': 'source_ratio',
                    'value': {
                        'field_group': "top_click+home_click+push_click",
                        'func': 'sum_ratio'
                    }
                }],
                'default_q': {'filters': [{
                    'name': 'date',
                    'op': '==',
                    'val': (n_days_ago, [1, '%Y-%m-%d'])
                }, {
                    'name': 'category',
                    'op': '==',
                    'val': 1
                }]},
                'chart_type': ChartType.Pie
            }],
            'filters': {
                'multi': [{
                    'model_id': '1005',
                    'name': 'source',
                }]
            }
        }, 'category_source_ratio_ru_ru': {
            'charts': [{
                'model_id': '2005',
                'x_dimension': 'source',
                'y_dimension': [{
                    'name': 'source_ratio',
                    'value': {
                        'field_group': "top_click+home_click+push_click",
                        'func': 'sum_ratio'
                    }
                }],
                'default_q': {'filters': [{
                    'name': 'date',
                    'op': '==',
                    'val': (n_days_ago, [1, '%Y-%m-%d'])
                }, {
                    'name': 'category',
                    'op': '==',
                    'val': 1
                }]},
                'chart_type': ChartType.Pie
            }],
            'filters': {
                'multi': [{
                    'model_id': '2005',
                    'name': 'source',
                }]
            }
        }, 'category_source_ratio_ja_jp': {
            'charts': [{
                'model_id': '3005',
                'x_dimension': 'source',
                'y_dimension': [{
                    'name': 'source_ratio',
                    'value': {
                        'field_group': "top_click+home_click+push_click",
                        'func': 'sum_ratio'
                    }
                }],
                'default_q': {'filters': [{
                    'name': 'date',
                    'op': '==',
                    'val': (n_days_ago, [1, '%Y-%m-%d'])
                }, {
                    'name': 'category',
                    'op': '==',
                    'val': 1
                }]},
                'chart_type': ChartType.Pie
            }],
            'filters': {
                'multi': [{
                    'model_id': '3005',
                    'name': 'source',
                }]
            }
        }, 'category_source_ratio_ar_sa': {
            'charts': [{
                'model_id': '4005',
                'x_dimension': 'source',
                'y_dimension': [{
                    'name': 'source_ratio',
                    'value': {
                        'field_group': "top_click+home_click+push_click",
                        'func': 'sum_ratio'
                    }
                }],
                'default_q': {'filters': [{
                    'name': 'date',
                    'op': '==',
                    'val': (n_days_ago, [1, '%Y-%m-%d'])
                }, {
                    'name': 'category',
                    'op': '==',
                    'val': 1
                }]},
                'chart_type': ChartType.Pie
            }],
            'filters': {
                'multi': [{
                    'model_id': '4005',
                    'name': 'source',
                }]
            }
        },
    }
}


app = multalisk.Multalisk(__name__)
app.init_conf(APP_CONF, debug=DEBUG)


class News_report_origin_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1001"
    __tablename__ = "report_origin_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2001"
    __tablename__ = "report_origin_ru_ru"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3001"
    __tablename__ = "report_origin_ja_jp"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_origin_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4001"
    __tablename__ = "report_origin_ar_sa"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1002"
    __tablename__ = "report_type_sum_tr_tr"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2002"
    __tablename__ = "report_type_sum_ru_ru"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3002"
    __tablename__ = "report_type_sum_ja_jp"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_type_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4002"
    __tablename__ = "report_type_sum_ar_sa"
    type = orm.Column(orm.VARCHAR(32), primary_key=True)
    click = orm.Column(orm.Integer)
    show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1003"
    __tablename__ = "report_category_sum_tr_tr"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2003"
    __tablename__ = "report_category_sum_ru_ru"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3003"
    __tablename__ = "report_category_sum_ja_jp"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_category_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4003"
    __tablename__ = "report_category_sum_ar_sa"
    category = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1004"
    __tablename__ = "report_priority_sum_tr_tr"
    priority = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2004"
    __tablename__ = "report_priority_sum_ru_ru"
    priority = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3004"
    __tablename__ = "report_priority_sum_ja_jp"
    priority = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_priority_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4004"
    __tablename__ = "report_priority_sum_ar_sa"
    priority = orm.Column(orm.Integer, primary_key=True)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1005"
    __tablename__ = "report_source_sum_tr_tr"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2005"
    __tablename__ = "report_source_sum_ru_ru"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3005"
    __tablename__ = "report_source_sum_ja_jp"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_source_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4005"
    __tablename__ = "report_source_sum_ar_sa"
    source = orm.Column(orm.VARCHAR(128), primary_key=True)
    category = orm.Column(orm.Integer)
    top_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_tr_tr(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "1006"
    __tablename__ = "report_news_sum_tr_tr"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ru_ru(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "2006"
    __tablename__ = "report_news_sum_ru_ru"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ja_jp(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "3006"
    __tablename__ = "report_news_sum_ja_jp"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


class News_report_news_ar_sa(object):
    __metaclass__ = app.MetaSQL
    __modelid__ = "4006"
    __tablename__ = "report_news_sum_ar_sa"
    news_id = orm.Column(orm.Integer, primary_key=True)
    category = orm.Column(orm.Integer)
    priority = orm.Column(orm.Integer)
    source = orm.Column(orm.VARCHAR(128))
    top_click = orm.Column(orm.Integer)
    recommend_click = orm.Column(orm.Integer)
    home_click = orm.Column(orm.Integer)
    push_click = orm.Column(orm.Integer)
    top_show = orm.Column(orm.Integer)
    recommend_show = orm.Column(orm.Integer)
    home_show = orm.Column(orm.Integer)
    push_show = orm.Column(orm.Integer)
    total_click = orm.Column(orm.Integer)
    total_show = orm.Column(orm.Integer)
    date = orm.Column(orm.VARCHAR(30), primary_key=True)


# init_cache(host='127.0.0.1', port=6379)

app.run(host='0.0.0.0', port=5000)
