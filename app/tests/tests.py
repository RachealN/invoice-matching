import pytest
from app import create_app
from unittest.mock import patch
from app.services.invoice_service import MatchingService
from app.models.invoice_line_item import InvoiceLineItem  
from app.models.delivery_line_item import DeliveryLineItem  


@pytest.fixture(scope="session")
def app_context():
    """
    Creates a Flask application context for the tests.
    """
    app = create_app()
    with app.app_context():
        yield app

@pytest.fixture
def mock_invoice_line_items(app_context):
    return [
        InvoiceLineItem(
            id=1,
            invoice_id="inv1", 
            delivery_number="D345",
            title="Macbook",
            unit="pcs",
            amount=2,
            price=1000.0
        ),
        InvoiceLineItem(
            id=2,
            invoice_id="inv2",  
            delivery_number="D456",
            title="iPhone",
            unit="pcs",
            amount=3,
            price=500.0
        ),
    ]

@pytest.fixture
def mock_delivery_line_items(app_context):
    return [
        DeliveryLineItem(
            id=1,
            delivery_number="D345",
            title="Macbook",
            unit="pcs",
            amount=2
        ),
        DeliveryLineItem(
            id=2,
            delivery_number="D456",
            title="iPhone",
            unit="pcs",
            amount=3
        ),
        DeliveryLineItem(
            id=3,
            delivery_number="D457", 
            title="iPhone",
            unit="pcs",
            amount=1
        )
    ]

def test_exact_matching(mock_invoice_line_items, mock_delivery_line_items, app_context):
    invoice_items = mock_invoice_line_items
    delivery_items = {item.delivery_number: item for item in mock_delivery_line_items}

    with patch("app.repositories.invoice_repository.InvoiceRepository.update_invoice") as mock_update:
        mock_update.return_value = None
        result = MatchingService.match_invoice_to_delivery(invoice_items, delivery_items)

    assert result["message"] == "Matching process completed"
    assert result["unmatched"] == 0
    assert invoice_items[0].delivery_id == 1  # Macbook matched   
    assert invoice_items[1].delivery_id == 2  # iPhone matched

def test_fuzzy_matching(mock_invoice_line_items, mock_delivery_line_items, app_context):
    invoice_items = mock_invoice_line_items
    delivery_items = {item.delivery_number: item for item in mock_delivery_line_items}

    with patch("app.services.invoice_service.MatchingService.find_best_match") as mock_fuzzy_match, \
         patch("app.repositories.invoice_repository.InvoiceRepository.update_invoice") as mock_update:
        mock_fuzzy_match.return_value = "D456"
        mock_update.return_value = None  # Prevent actual DB commit
        result = MatchingService.match_invoice_to_delivery(invoice_items, delivery_items)

    assert result["message"] == "Matching process completed"
    assert result["unmatched"] == 0
    assert invoice_items[1].delivery_id == 2


def test_unmatched_invoices(mock_invoice_line_items, mock_delivery_line_items, app_context):
    unmatched_delivery = DeliveryLineItem(
        id=4,
        delivery_number="D999", 
        title="Tablet",
        unit="pcs",
        amount=1
    )
    invoice_items = mock_invoice_line_items
    delivery_items = {item.delivery_number: item for item in mock_delivery_line_items}
    delivery_items["D999"] = unmatched_delivery

    with patch("app.repositories.invoice_repository.InvoiceRepository.update_invoice") as mock_update:
        mock_update.return_value = None
        result = MatchingService.match_invoice_to_delivery(invoice_items, delivery_items)

    assert result["message"] == "Matching process completed"
    assert result["unmatched"] >= 0

def test_multiple_line_items_per_delivery(mock_invoice_line_items, mock_delivery_line_items, app_context):
    delivery_items = [
        DeliveryLineItem(id=1, delivery_number="D345", title="Macbook", unit="pcs", amount=2),
        DeliveryLineItem(id=2, delivery_number="D345", title="Macbook", unit="pcs", amount=1),
    ]
    invoice_items = mock_invoice_line_items
    delivery_items_dict = {item.delivery_number: item for item in delivery_items}

    with patch("app.repositories.invoice_repository.InvoiceRepository.update_invoice") as mock_update:
        mock_update.return_value = None
        result = MatchingService.match_invoice_to_delivery(invoice_items, delivery_items_dict)

    assert result["message"] == "Matching process completed"
    assert result["unmatched"] == 1 