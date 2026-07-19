# Business Impact Guidelines

## Purpose

This document explains how business metrics should be interpreted and how planners should respond to inventory conditions.

---

# Potential Lost Sales

## Definition

Potential Lost Sales = max(0, Forecast Demand - Current Inventory)

## Business Meaning

Represents units that may not be sold because inventory is insufficient.

## Interpretation

### Value = 0

Current inventory is sufficient to support forecast demand.

### Value > 0

Inventory shortage may result in lost sales opportunities.

## Recommended Response

* Review inventory availability
* Evaluate replenishment options
* Monitor forecast changes

---

# Revenue Risk

## Definition

Revenue Risk = Potential Lost Sales × Selling Price

## Business Meaning

Represents potential revenue exposure caused by inventory shortages.

## Interpretation

### Value = 0

No forecasted revenue exposure.

### Value > 0

Revenue may be lost if demand cannot be fulfilled.

## Recommended Response

* Prioritize inventory review
* Assess replenishment urgency
* Escalate if exposure becomes significant

---

# Inventory At Risk

## Definition

Inventory At Risk = max(0, Projected Inventory - Reorder Point)

## Business Meaning

Represents inventory that may become excess inventory.

## Interpretation

### Value = 0

Inventory remains within expected operating levels.

### Value > 0

Inventory may exceed planned requirements.

## Recommended Response

* Review purchasing activity
* Monitor inventory turnover
* Evaluate inventory reduction opportunities

---

# Recommended Order Quantity

## Definition

Recommended Order Quantity = max(0, Reorder Point - Current Inventory)

## Business Meaning

Represents the quantity required to reach the target inventory position.

## Interpretation

### Value = 0

No replenishment required.

### Value > 0

Inventory replenishment should be evaluated.

## Recommended Response

* Review inventory plan
* Validate forecast assumptions
* Consider replenishment timing

---

# Inventory Health Score

## Definition

Inventory Health Score is a business-facing indicator of overall inventory condition.

## Score Bands

### 90 - 100

Excellent

### 70 - 89

Healthy

### 50 - 69

Monitor

### 30 - 49

At Risk

### 0 - 29

Critical

## Business Meaning

Higher scores indicate healthier inventory conditions.

Lower scores indicate increased operational risk.

## Recommended Response

### Excellent

Continue routine monitoring.

### Healthy

Monitor inventory performance.

### Monitor

Review inventory trends regularly.

### At Risk

Investigate inventory risks and create action plan.

### Critical

Immediate review and management attention required.
