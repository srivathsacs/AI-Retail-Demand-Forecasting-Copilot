# Inventory Risk Policy

## Purpose

This document defines inventory risk levels, business interpretation, and required actions for inventory planning decisions.

---

# Stockout Risk

## CRITICAL Stockout Risk

### Risk Code

STOCKOUT_CRITICAL

### Definition

Inventory Gap < -Safety Stock

### Business Interpretation

Projected inventory is significantly below required safety stock levels.

### Potential Impact

* Severe inventory shortage
* High probability of lost sales
* Customer service disruption

### Required Actions

* Immediate inventory review
* Create replenishment order
* Escalate to management

### Response Time

Within 24 hours

---

## HIGH Stockout Risk

### Risk Code

STOCKOUT_HIGH

### Definition

Inventory Gap < 0

### Business Interpretation

Projected inventory falls below safety stock.

### Potential Impact

* Increased stockout probability
* Potential lost sales

### Required Actions

* Review inventory position
* Evaluate replenishment options
* Monitor forecast changes

### Response Time

Within 2 business days

---

## MEDIUM Stockout Risk

### Risk Code

STOCKOUT_MEDIUM

### Definition

Inventory Gap < 25% of Safety Stock

### Business Interpretation

Inventory remains above safety stock but available buffer is limited.

### Potential Impact

* Elevated future stockout risk
* Reduced inventory protection

### Required Actions

* Monitor inventory position
* Review forecast updates

### Response Time

Within 7 business days

---

## LOW Stockout Risk

### Risk Code

STOCKOUT_LOW

### Definition

Inventory Gap >= 25% of Safety Stock

### Business Interpretation

Inventory position remains healthy.

### Potential Impact

* Minimal stockout exposure

### Required Actions

* Continue normal monitoring

### Response Time

Routine review

---

# Overstock Risk

## HIGH Overstock Risk

### Risk Code

OVERSTOCK_HIGH

### Definition

Projected Inventory > 4 × Safety Stock

### Business Interpretation

Inventory levels significantly exceed expected requirements.

### Potential Impact

* Excess inventory holding costs
* Increased markdown risk

### Required Actions

* Review purchasing plans
* Evaluate inventory reduction opportunities

---

## MEDIUM Overstock Risk

### Risk Code

OVERSTOCK_MEDIUM

### Definition

Projected Inventory > 3 × Safety Stock

### Business Interpretation

Inventory exceeds normal operating levels.

### Potential Impact

* Increased carrying costs

### Required Actions

* Monitor inventory trends

---

## LOW Overstock Risk

### Risk Code

OVERSTOCK_LOW

### Definition

Projected Inventory <= 3 × Safety Stock

### Business Interpretation

Inventory levels remain within acceptable limits.

### Required Actions

* Continue standard inventory review
