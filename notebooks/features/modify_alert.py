"""
During the ingets process, the alert with diaSource/prvDiaSources is modified to 
a single diaSourcesList, which is passed down the line.
This code is essentailly a copy of lasair-lsst/pipeline/ingest/ingest.py line 278 et seq
"""
def modify(lsst_alert):
    diaObject          = lsst_alert.get('diaObject', None)
    ssObject           = lsst_alert.get('ssObject', None)

    diaSourcesList = [lsst_alert['diaSource']]
    if 'prvDiaSources' in lsst_alert and lsst_alert['prvDiaSources']:
        diaSourcesList = diaSourcesList + lsst_alert['prvDiaSources']
    else:
        diaSourcesList = []

    if 'prvDiaForcedSources' in lsst_alert and lsst_alert['prvDiaForcedSources']:
        diaForcedSourcesList = lsst_alert['prvDiaForcedSources']
    else:
        diaForcedSourcesList = []

    if 'prvDiaNondetectionLimits' in lsst_alert and lsst_alert['prvDiaNondetectionLimits']:
        diaNondetectionLimitsList = lsst_alert['prvDiaNondetectionLimits']
    else:
        diaNondetectionLimitsList = []

    if 'dec' in diaObject:
        diaObject['decl'] = diaObject['dec']
        del diaObject['dec']
    for diaSource in diaSourcesList:
        if 'dec' in diaSource:
            diaSource['decl'] = diaSource['dec']
            del diaSource['dec']
    for diaForcedSource in diaForcedSourcesList:
        if 'dec' in diaForcedSource:
            diaForcedSource['decl'] = diaForcedSource['dec']
            del diaForcedSource['dec']


    diaObject['ebv'] = 0.0

    alert = {
        'diaObject': diaObject,
        'diaSourcesList': diaSourcesList,
        'diaForcedSourcesList': diaForcedSourcesList,
        'diaNondetectionLimitsList': diaNondetectionLimitsList,
        'ssObject': ssObject,
    }
    return alert
