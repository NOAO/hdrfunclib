# Python library
import logging
# External packages
import astropy.io.fits as pyfits
# Local packages
from hdrfunclib.personalities import personalities


def flat_hdudict(hdudict_list):
    """Combine key/value pairs from all HDUs into a single dict (returned).
    If key appears in multiple HDUs, first one wins."""
    hdudict = dict()
    for hdict in hdudict_list:
        for k,v in hdict.items():
            if k not in hdudict:
                hdudict[k] = v
    return hdudict

class Personality():
    
    def __init__(self, persName):
        # list of name/dict pairs should be same as dict formed from them
        # (unless a key is being overwritten)
        if len(dict(personalities)) != len(personalities)):
            raise Exception('Duplicate personality name!')
        
        self.persdict = dict()    # like CONTENT of old Personality File
        self.persName = '<none>'  # like NAME    of old Personality File
        self.update0dict = dict() # k/v to update on HDU-0

        if persName in personalities:
            self.persdict = personalities.get(persName)
            self.persName = persName
        else:
            msg = ('Personality name ("{}") not found.  Available personalties'
                   ' are: {}'
                   ' To add more, see hdrfunclib/personalities'
                   ).format(', '.join(personalities.keys()))
            raise NoPersonalityName(msg)

    def name(self):
        return self.persName

    def options(self):
        return self.persdict['options'].items()

    def params(self):
        return self.persdict['params'].items()

    def param(self, name):
        if params not in self.persdict:
            return None
        return self.persdict.get('params').get(name)

    def functions(self):
        return self.persdict.get('calchdr',[])
    
    def make_update_dict(self, hdu_dict_list):
        """Apply personality to flattened header"""
        # Flatten all HDUs into single (hdu0dict)
        #!print('DBG: hdudict_list={}'.format(pformat(hdudict_list)))
        hdudict = flat_hdudict(hdu_dict_list)

        # Apply personality "options" (direct field values)
        for k,v in self.options():
            # overwrite with explicit fields from personality
            hdudict[k] = v  

        # Apply hdr funcs
        for calcfunc in self.functions():
            new = calcfunc(hdudict)
            logging.info('Ran hdrfunc: {}=>{}'.format(calcfunc.__name__, new))
            hdudict.update(new)
        self.update0dict = hdudict
        return hdudict

    def modify_fits(self, orig_fits_fname, new_fits_fname):
        with pyfits.open(orig_fits_fname) as hdulist:
            hdulist[0].header.update(self.update0dict)
            hdulist.writeto(new_fits_fname, output_verify='fix')
        return new_fits_fname
        
