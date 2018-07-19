#! /usr/bin/env python3
"""
Every hdrfunc must have same
"""

# Grouped by OUTPUT Keyword

import logging
from .hdr_decorators import inkws, outkws


#########################
### DTSERNO
###

@inkws(['DETSERNO'])
@outkws(['DTSERNO'])
def DETSERNOtoDTSERNO(orig, **kwargs):
    """Intended for soar-spartan FITS files. Allow DETSERNO to be missing."""
    return {'DTSERNO': orig['DETSERNO'].strip()}

#########################
### DATE-OBS
###

@inkws(['UTSHUT'])
@outkws(['DATE-OBS'])
def fixTriplespec(orig, **kwargs):
    """Fix triplespec DATE-OBS using UTSHUT (Universal Time SHUTter)"""
    new = {'DATE-OBS': orig['UTSHUT'],
           #'INSTRUME': orig['INSTRUM'],
    }
    logging.debug('fixTriplespec: fields DATE-OBS ({})'
                  #', INSTRUME ({})'
                  #.format(new['DATE-OBS'], new['INSTRUME']))
                  .format(new['DATE-OBS']))
    return  new


@inkws(['DATE-OBS', 'TIME-OBS'])
@outkws(['DATE-OBS'])
def addTimeToDATEOBS(orig, **kwargs):
    """Use TIME-OBS for time portion of DATEOBS."""
    if ('T' in orig['DATE-OBS']): 
        return {'DATE-OBS': orig['DATE-OBS']}
    else:
        return {'DATE-OBS': orig['DATE-OBS'] + 'T' + orig['TIME-OBS']}


@inkws(['DATE-OBS', 'DATE'])
@outkws(['ODATEOBS', 'DATE-OBS'])
def DATEOBSfromDATE(orig, **kwargs):
    """hdr function: DATEOBSfromDATE"""
    if 'ODATEOBS' in orig:
        logging.info('Overwriting existing ODATEOBS!')
    return {'ODATEOBS': orig['DATE-OBS'],            # save original
            'DATE-OBS': orig['DATE']+'.0' }


#########################
### DTCALDAT
###

@inkws(['DATE-OBS'])
@outkws(['DTCALDAT'])
def DTCALDATfromDATEOBStus(orig, **kwargs):
    """hdr function: DTCALDATfromDATEOBStus"""
    from dateutil import tz
    import datetime as dt

    local_zone = tz.gettz('America/Phoenix')
    utc = dt.datetime.strptime(orig['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    utc = utc.replace(tzinfo=tz.tzutc()) # set UTC zone
    localdt = utc.astimezone(local_zone)
    if localdt.time().hour > 9:
        caldate = localdt.date()
    else:
        caldate = localdt.date() - dt.timedelta(days=1)
    #!logging.debug('localdt={}, DATE-OBS={}, caldate={}'
    #!              .format(localdt, orig['DATE-OBS'], caldate))
    new = {'DTCALDAT': caldate.isoformat()}
    return new


@inkws(['DATE-OBS'])
@outkws(['DTCALDAT'])
def DTCALDATfromDATEOBSchile(orig, **kwargs):
    """hdr function: DTCALDATfromDATEOBSchile"""
    from dateutil import tz
    import datetime as dt

    local_zone = tz.gettz('Chile/Continental')
    utc = dt.datetime.strptime(orig['DATE-OBS'], '%Y-%m-%dT%H:%M:%S.%f')
    utc = utc.replace(tzinfo=tz.tzutc()) # set UTC zone
    localdt = utc.astimezone(local_zone)
    if localdt.time().hour > 12:
        caldate = localdt.date()
    else:
        caldate = localdt.date() - dt.timedelta(days=1)
    logging.debug('localdt={}, DATE-OBS={}, caldate={}'
                  .format(localdt, orig['DATE-OBS'], caldate))
    new = {'DTCALDAT': caldate.isoformat()}
    return new


#########################
### DTPROPID
###

@inkws(['PROPID'])
@outkws(['DTPROPID'])
def PROPIDplusCentury(orig, **kwargs):
    """Add missing century"""
    return {'DTPROPID': '20' + orig.get('PROPID','NA').strip('"') }


#########################
### DTINSTR
###

@inkws(['INSTRUME'])
@outkws(['DTINSTRU'])
def INSTRUMEtoDT(orig, **kwargs):
    """hdr function: INSTRUMEtoDT"""
    if 'DTINSTRU' in orig:
        return {'DTINSTRU': orig['DTINSTRU'] }
    else:
        return {'DTINSTRU': orig['INSTRUME'] }


#########################
### OBSTYPE
###

@inkws(['IMAGETYP'])
@outkws(['OBSTYPE'])
def IMAGTYPEtoOBSTYPE(orig, **kwargs):
    """hdr function: IMAGTYPEtoOBSTYPE"""
    return {'OBSTYPE': orig['IMAGETYP']  }


#########################
### OBSID
###

@inkws(['DATE-OBS'])
@outkws(['OBSID'])
def bokOBSID(orig, **kwargs):
    """hdr function: bokOBSID"""
    return {'OBSID': 'bok23m.'+orig['DATE-OBS'] }

