"""Constants for document categorization."""

from typing import Dict, List

# Default category hierarchy
DEFAULT_CATEGORIES = {
    'procedural': {
        'name': 'Procedural Documents',
        'subcategories': {
            'notice': {
                'name': 'Notice of Arbitration',
                'keywords': ['notice', 'request for arbitration', 'initiation', 'commence']
            },
            'orders': {
                'name': 'Procedural Orders',
                'keywords': ['order', 'directive', 'schedule', 'procedural']
            },
            'terms': {
                'name': 'Terms of Reference',
                'keywords': ['terms of reference', 'scope', 'framework', 'procedure']
            }
        }
    },
    'submissions': {
        'name': 'Submissions and Pleadings',
        'subcategories': {
            'written': {
                'name': 'Written Submissions',
                'keywords': ['statement', 'submission', 'memorial', 'brief']
            },
            'memorials': {
                'name': 'Memorials',
                'keywords': ['memorial', 'counter-memorial', 'reply', 'rejoinder']
            },
            'jurisdictional': {
                'name': 'Jurisdictional Submissions',
                'keywords': ['jurisdiction', 'competence', 'admissibility']
            }
        }
    },
    'evidence': {
        'name': 'Evidentiary Materials',
        'subcategories': {
            'witness': {
                'name': 'Witness Evidence',
                'keywords': ['witness statement', 'testimony', 'declaration', 'affidavit']
            },
            'documentary': {
                'name': 'Documentary Evidence',
                'keywords': ['exhibit', 'document', 'record', 'correspondence']
            },
            'expert': {
                'name': 'Expert Materials',
                'keywords': ['expert report', 'analysis', 'opinion', 'assessment']
            }
        }
    },
    'awards': {
        'name': 'Award Documents',
        'subcategories': {
            'interim': {
                'name': 'Interim Awards',
                'keywords': ['interim award', 'preliminary', 'provisional', 'temporary']
            },
            'final': {
                'name': 'Final Awards',
                'keywords': ['final award', 'award on merits', 'costs award', 'interest']
            },
            'consent': {
                'name': 'Consent Awards',
                'keywords': ['consent award', 'settlement', 'agreed terms', 'voluntary']
            }
        }
    },
    'administrative': {
        'name': 'Administrative Documents',
        'subcategories': {
            'communications': {
                'name': 'Communications',
                'keywords': ['letter', 'email', 'correspondence', 'notice']
            },
            'financial': {
                'name': 'Financial Documents',
                'keywords': ['costs', 'fees', 'deposit', 'payment']
            },
            'logistical': {
                'name': 'Logistical Documents',
                'keywords': ['hearing', 'meeting', 'schedule', 'arrangement']
            }
        }
    }
}

# Confidence thresholds for classification
CONFIDENCE_THRESHOLDS = {
    'primary': 0.7,    # Threshold for primary category assignment
    'secondary': 0.5,  # Threshold for secondary category assignment
    'review': 0.4      # Threshold below which manual review is required
}

# Language detection confidence threshold
LANGUAGE_CONFIDENCE_THRESHOLD = 0.8

# Maximum document size for processing (in bytes)
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB