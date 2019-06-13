"""\
Used on top of hdr_function defintions to do some automatic bookkeeping.

These decorators will:
- Add to a global var (all_in_keywords, all_out_keywords) that is the set
  of all FITS keywords in the @inkws or @outkws of any calcfunc.

- Rename the decorated (wrapped) function to "__<originalName>"

- add attributes to decorated function: inkwset, outkwset

- Cause wrapped function to raise error if at the time it is called the
  prerequisit FITS *input* keywords (inkws) are not in the header.

- Cause wrapped function to raise error if at the time it is called the
  prerequisit FITS *output keywords (outkws) are not in returned by the 
  wrapped function.

"""

all_in_keywords = set()
all_out_keywords = set()


class inkws(object):
    def __init__(self,kwlist):
        global all_in_keywords
        self.inkwset = set(kwlist)
        all_in_keywords.update(self.inkwset)

    def __call__(self, f):
        origfuncname = f.__name__
        #!print('f={}, f.name={}'.format(f, f.__name__))

        def wrapped_f(orig, **kwargs):
            origkws = set(orig.keys())
            if not self.inkwset.issubset(origkws):
                missing = self.inkwset.difference(origkws)
                msg = ('Some keywords required per @inkws [{}] are missing'
                       ' in orig keys [{}].'
                       ' SOLUTIONS: Fix FITS, change HDR FUNC @inkws')
                raise Exception(msg.format(', '.join(missing),
                                           ', '.join(origkws)))
            else:
                return f(orig, **kwargs)
        wrapped_f.__name__ = '_' + origfuncname
        wrapped_f.inkwset = self.inkwset
        return wrapped_f
            

class outkws(object):
    def __init__(self,kwlist):
        global all_out_keywords
        self.outkwset = set(kwlist)
        all_out_keywords.update(self.outkwset)

    def __call__(self, f):
        origfuncname = f.__name__
        #!print('f={}, f.name={}'.format(f, f.__name__))

        def wrapped_f(orig, **kwargs):
            new = f(orig, **kwargs)
            if not self.outkwset.issubset(new.keys()):
                missing = self.outkwset.difference(new.keys())
                msg = ('Some keywords ({}) required per @outkws ({}) '
                       'are missing in hdrfunc return value.'
                       ' SOLUTIONS: Fix FITS, or change HDR FUNC @outkws')
                raise Exception(msg.format(', '.join(missing),
                                           ', '.join(self.outkwset)))
            else:
                return new
        wrapped_f.__name__ = '_' + origfuncname
        wrapped_f.outkwset = self.outkwset
        return wrapped_f
            
