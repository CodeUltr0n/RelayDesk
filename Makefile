.PHONY: test eval eval-relaydesk eval-heldout

test:
	python -m pytest -q

eval:
	python scripts/run_eval.py --cases fixtures/cases --pipeline null

eval-relaydesk:
	python scripts/run_eval.py --cases fixtures/cases --pipeline relaydesk --split dev

eval-heldout:
	python scripts/run_eval.py --cases fixtures/cases --pipeline relaydesk --split heldout
