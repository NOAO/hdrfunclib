import hdrfunclib.hdr_decorators as hd
import hdrfunclib.hdr_funcs as hf



    # from: sandbox/tada-cli/personalities/*/*.yaml
    # All DTTELESC, DTINSTRU should be lowercase
personalities = {
    'default': {
        'options': {},
        'calchdr': [],
        'params':  {},
    },

    'kp4m-kosmos': {
        'options': {
            'DTINSTRU': 'kosmos',
            'DTSITE': 'kp',
            'DTTELESC': 'kp4m',
            'PROCTYPE': 'raw',
            'PRODTYPE': 'image',
            },
        'calchdr': [hf.DTCALDATfromDATEOBStus],
        'params':  {},
        },
    'wiyn-bench': {
        'options': {
            'DTINSTRU': 'bench',
            'DTSITE':   'kp',
            'DTTELESC': 'wiyn',
            'PROCTYPE': 'raw',
            'PRODTYPE': 'image',
        },
        'calchdr': [hf.IMAGTYPEtoOBSTYPE,
                    hf.DTCALDATfromDATEOBStus,
        ],
        'params': { },
    },

    'wiyn-whirc': {
        'options': {
            'DTINSTRU': 'whirc',
            'DSITE':    'kp',
            'DTTELESC': 'wiyn',
            'PROCTYPE': 'raw',
            'PRODTYPE': 'image',
        },
        'calchdr': [hf.IMAGTYPEtoOBSTYPE,
                    hf.DTCALDATfromDATEOBStus,
        ],
        'params': { },
    },
}
    
