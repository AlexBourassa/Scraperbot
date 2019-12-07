# RSS Feeds
class Feed(object):
    def __init__(self, url, journal_name=None, journal_abbrv=None, journal_img=None):
        self.url = url
        self.journal_name = journal_name
        self.journal_abbrv = journal_abbrv
        self.journal_img = journal_img

feeds = [
    Feed('http://feeds.aps.org/rss/recent/prl.xml', 'Physical Review Letters', 'PRL', 'img/aps.png'),
    Feed('http://feeds.aps.org/rss/recent/prx.xml', 'Physical Review X', 'PRX', 'img/aps.png'),
    Feed('http://feeds.aps.org/rss/recent/prapplied.xml', 'Physical Review Applied', 'PR', 'img/aps.png'),
    Feed('http://feeds.aps.org/rss/recent/pra.xml', 'Physical Review A', 'PRA', 'img/aps.png'),
    Feed('http://www.sciencemag.org/rss/current.xml', 'Science', 'Science', 'img/science.png'),
    Feed('http://advances.sciencemag.org/rss/current.xml', 'Science Advance', 'Sci. Adv.','img/science advance.jpg'),
    Feed('http://feeds.nature.com/nature/rss/current', 'Nature', 'Nature', 'img/nature.png'),
    Feed('http://feeds.nature.com/nphoton/rss/current', 'Nature Photonics', 'Nat. Phot.', 'img/nature.png'),
    Feed('http://feeds.nature.com/nnano/rss/current', 'Nature Nanotechnology', 'Nat. Nano.', 'img/nature.png'),
    Feed('http://feeds.nature.com/nmat/rss/current', 'Nature Material', 'Nat. Mat.', 'img/nature.png'),
    Feed('http://feeds.nature.com/nphys/rss/current', 'Nature Physics', 'Nat. Phys.', 'img/nature.png'),
    Feed('http://aip.scitation.org/action/showFeed?type=etoc&feed=rss&jc=apl', 'Applied Physics Letters', 'APL', 'img/aip.png'),
    Feed('http://aip.scitation.org/action/showFeed?type=etoc&feed=rss&jc=jap', 'Journal of Applied Physics', 'Journal of Applied Physics', 'img/aip.png'),
    Feed('http://feeds.feedburner.com/acs/apchd5','ACS Photonics','ACS Phot.', 'img/acs.png'),
    Feed('http://feeds.feedburner.com/acs/nalefd','ACS Nano Letter','NanoLetter', 'img/acs.png'),
    Feed('http://feeds.nature.com/npjqi/rss/current','NPJ Quantum Information','NPJQI', 'img/npj.jpg'),
]

"""
feeds = ('http://feeds.aps.org/rss/tocsec/PRL-AtomicMolecularandOpticalPhysics.xml',\
    'http://feeds.aps.org/rss/tocsec/PRL-CondensedMatterElectronicPropertiesetc.xml',\
    'http://feeds.aps.org/rss/tocsec/PRL-CondensedMatterStructureetc.xml',\
    'http://feeds.aps.org/rss/topics/spintronics.xml',\
    'http://feeds.aps.org/rss/recent/prx.xml',\
    'http://feeds.aps.org/rss/recent/prapplied.xml',\
    'http://feeds.aps.org/rss/recent/prb.xml',\
    'http://feeds.aps.org/rss/recent/pra.xml',\
     'http://www.sciencemag.org/rss/current.xmlhttp://advances.sciencemag.org/rss/current.xml',\
     'http://feeds.nature.com/nphoton/rss/current',\
     'http://feeds.nature.com/nnano/rss/current',\
     'http://feeds.nature.com/nmat/rss/current',\
      'http://feeds.nature.com/nphys/rss/current',\
     'http://feeds.nature.com/nature/rss/current',\
     'http://scitation.aip.org/rss/content/aip/journal/apl/latestarticles?fmt=rss',\
     'http://feeds.feedburner.com/acs/apchd5',\
     'http://feeds.feedburner.com/acs/nalefd')
"""

# ArXiV categories
cats = ('quant-ph', 'cond-mat.mtrl-sci', 'physics.optics', 'physics.atom-ph')

# Buzzwords
buzzwords = [
        'defect spin',
        'spin defect',
        'spin qubit',
        'single defect',
        'color center',

        'silicon carbide',
        ' SiC ',

        'divacancies',
        'divacancy',
        'VV0',
        ' SiV ',
        'silicon vacancies',
        'silicon vacancy',
        ' NV ',
        'N-V',

        # 'optomechanics',
        # 'nanomechanics',
        # 'optomechanical',
        # 'nanomechanical',

        'strong coupling',
        'diamond',
        'hybrid quantum',
        'ODMR',
        'awschalom',
        'schuster',
        'dyakanov',
        'lukin',
        'jayich',
        'cleland',
        'schoelkopf',
        'budker',
        'wrachtrup',
        'hanson',
        'taminiau',
        'childress',
        'sankey',
        'kippenberg',
        'englund',

        'quantum computing',

        'rare earth ion',
        'hybrid quantum system',
        'DNP',
        'spin-strain',
        'cQED',
        'defect laser',
        'phonon laser',
        'electroluminescence',
        'defect charge state',
        'spin dependent recombination',
        'EDMR',
        'spin-to-charge',
        'spin to charge',
        'lifetime limited',
        'spectral diffusion',
        'long-distance entanglement',
        'remote entanglement',
        'quantum communication',
        ]
