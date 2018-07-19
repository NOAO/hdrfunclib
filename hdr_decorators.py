import tada.exceptions as tex

all_in_keywords = set()
all_out_keywords = set()

class inkws(object):
    def __init__(self,kwlist):
        global all_in_keywords
        self.inkwset = set(kwlist)
        
        all_in_keywords.update(self.inkwset)

    def __call__(self, f):
        def wrapped_f(orig, **kwargs):
            origkws = set(orig.keys())
            if not self.inkwset.issubset(origkws):
                missing = self.inkwset.difference(origkws)
                msg = ('Some keywords required per @inkws [{}] are missing'
                       ' in [{}]. SOLUTIONS: Fix FITS, change HDR FUNC @inkws')
                #!return(msg.format(', '.join(missing), ', '.join(origkws)))
                raise tex.BadHdrFunc(msg.format(', '.join(missing),
                                                ', '.join(origkws)))
            else:
                return f(orig, **kwargs)
        return wrapped_f
            

class outkws(object):
    def __init__(self,kwlist):
        global all_out_keywords
        self.outkwset = set(kwlist)
        all_out_keywords.update(self.outkwset)

    def __call__(self, f):
        def wrapped_f(orig, **kwargs):
            new = f(orig, **kwargs)
            if not self.outkwset.issubset(new.keys()):
                missing = self.outkwset.difference(new.keys())
                msg = ('Some keywords ({}) required per @outkws ({}) '
                       'are missing in hdrfunc return value.'
                       ' SOLUTIONS: Fix FITS, or change HDR FUNC @outkws')
                #!return(msg.format(', '.join(missing), self.outkwset))
                raise tex.BadHdrFunc(msg.format(', '.join(missing),
                                                ', '.join(self.outkwset)))
            else:
                return new
        return wrapped_f
            
