# table-reservation-system
A system to manage a hotel's takeaway service

PROBLEM STATEMENT:
A hotel wants to develop a system to manage their takeaway service.
 The system should maintain the menu of the day. From the customer end,
 the system should be able to assign tokens for the registered orders and
 display the bill amount. After receiving the payment, the order should be
 confirmed and notified to the customer and the hotel manager. Appending
 the order should be disabled after payment. From the hotel manager's end,
 orderwise and item-wise lists should be displayed. Orders with 3 or less
 than 3 items can be given higher priority. The availability of a food item
 should be updated for the manager and the customer (during ordering).
 When the order is ready, a notification should be sent to the customer to
 collect their order.

DESIGN PATTERNS:
 Seat Reservation- State Pattern
 Notification- Observer Pattern, Decorator Pattern
 Manager- Singleton Pattern
 Mode of Payment- Strategy Pattern
 Cancel Reservation- Command Pattern
