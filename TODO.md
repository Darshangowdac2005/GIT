# TODO: Fix Claim Filing and Pending Claims Issues

## Backend Fixes
- [x] Verify claim submission in backend/routes/item_routes.py: Ensure claim insertion and item status update to 'claim_pending' works correctly.
- [x] Verify admin pending claims retrieval in backend/routes/admin_routes.py: Ensure pending claims are fetched correctly.
- [x] Verify claim resolution in backend/routes/admin_routes.py: Ensure approval updates claim to 'approved', item to 'resolved', and sends notifications; rejection updates claim to 'rejected'.

## Frontend Fixes
- [x] Verify claim submission UI in frontend/components/item_card.py: Ensure dialog submits claim and shows feedback.
- [x] Verify claim API call in frontend/api_client.py: Ensure claim_item_api posts correctly.
- [x] Verify admin dashboard pending claims loading in frontend/views/admin_dashboard.py: Ensure list loads and refreshes after resolution.
- [x] Verify home view item filtering in frontend/views/home_view.py: Modify to include resolved items in a "Solved Cases" section.
- [x] Add new endpoint or modify existing to fetch resolved items for solved cases list.
- [x] Ensure UI refreshes after claim submission and resolution using pubsub.

## Testing
- [ ] Test full flow: File claim, admin approves, item becomes resolved, solved cases list updates.
