"""Mock data for TechVision vs GlobalNet case testing."""

CASE_DATA = {
    "case_details": {
        "case_number": "LX-2024-0127",
        "claimant": "TechVision Systems Inc.",
        "respondent": "GlobalNet Solutions Ltd.",
        "dispute_nature": "Breach of Software Development Agreement",
        "amount": 2500000,
        "applicable_law": "English Law",
        "seat": "London, UK",
        "language": "English",
        "arbitrators": 3
    },
    "initial_documents": [
        {
            "title": "Notice of Arbitration",
            "file_name": "notice_of_arbitration.pdf",
            "category": "Procedural Documents",
            "date": "2024-01-27"
        },
        {
            "title": "Software Development Agreement",
            "file_name": "development_agreement.pdf",
            "category": "Contracts",
            "date": "2023-03-01"
        },
        {
            "title": "Statement of Claim",
            "file_name": "statement_of_claim.pdf",
            "category": "Submissions",
            "date": "2024-01-27"
        }
    ],
    "document_requests": [
        {
            "request_id": "REQ-001",
            "from_email": "tribunal@lexarb.com",
            "to_email": "case-lx20240127@lexarb.com",
            "subject": "Document Request - Technical Specifications",
            "date": "2024-01-30",
            "requested_documents": [
                "Original technical specifications (March 15, 2023)",
                "Subsequent specification revisions",
                "Change request logs (March-December 2023)",
                "Related email communications"
            ],
            "deadline": "2024-02-13"
        }
    ],
    "document_submissions": [
        {
            "submission_id": "SUB-001",
            "request_id": "REQ-001",
            "from_email": "techvision.legal@company.com",
            "date": "2024-02-10",
            "documents": [
                {
                    "file_name": "TechSpec_v1.0_15Mar2023.pdf",
                    "version": "1.0",
                    "date": "2023-03-15"
                },
                {
                    "file_name": "TechSpec_v1.1_30Apr2023.pdf",
                    "version": "1.1",
                    "date": "2023-04-30"
                },
                {
                    "file_name": "TechSpec_v2.0_15Jul2023.pdf",
                    "version": "2.0",
                    "date": "2023-07-15"
                },
                {
                    "file_name": "ChangeLog_Mar-Dec2023.xlsx",
                    "type": "Change Log",
                    "date_range": "2023-03-01/2023-12-31"
                }
            ]
        }
    ],
    "expected_categorization": {
        "TechSpec_v2.0_15Jul2023.pdf": {
            "document_type": "Technical Documentation",
            "relevance": "High",
            "award_sections": [
                "Background of Dispute",
                "Technical Requirements",
                "Timeline of Events"
            ],
            "metadata": {
                "date_range": "March 2023 - December 2023",
                "key_participants": [
                    "Project Manager",
                    "Technical Lead",
                    "Client Representative"
                ],
                "version_control": True
            }
        }
    }
}