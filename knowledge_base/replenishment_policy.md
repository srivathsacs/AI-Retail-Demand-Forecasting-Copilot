# Replenishment Policy

## Purpose

This document defines replenishment guidelines based on forecast demand, inventory position, and inventory risk metrics.

---

# Safety Stock Policy

## Definition

Safety Stock is reserve inventory maintained to protect against forecast uncertainty, supplier delays, and demand spikes.

## Planning Principle

Inventory should remain above Safety Stock whenever possible.

## Business Impact

Falling below Safety Stock increases stockout risk and potential lost sales exposure.

---

# Inventory Gap Policy

## Definition

Inventory Gap = Projected Inventory - Safety Stock

## Interpretation

### Positive Inventory Gap

Inventory remains above Safety Stock.

### Negative Inventory Gap

Inventory has breached Safety Stock and replenishment review is required.

---

# Reorder Review Guidelines

## LOW Stockout Risk

### Action

Continue routine inventory monitoring.

### Replenishment Decision

No immediate action required.

---

## MEDIUM Stockout Risk

### Action

Review forecast updates and inventory position.

### Replenishment Decision

Evaluate replenishment options if forecast demand increases.

---

## HIGH Stockout Risk

### Action

Perform inventory review immediately.

### Replenishment Decision

Prepare replenishment recommendation.

---

## CRITICAL Stockout Risk

### Action

Immediate replenishment review required.

### Replenishment Decision

Create replenishment order and escalate inventory shortage risk.

---

# Recommended Order Quantity

## Definition

Recommended Order Quantity = max(0, Reorder Point - Current Inventory)

## Planning Principle

Order recommendations should be based on inventory requirements rather than fixed order sizes.

---

# Forecast Dependency

## Policy

All replenishment decisions should use the latest approved demand forecast.

## Reason

Inventory recommendations are only as reliable as the forecast used to generate them.
