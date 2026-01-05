package com.polyglot.orderservice.domain.model;

public enum OrderStatus {
    PENDING,
    APPROVED,       
    RISK_DETECTED,
    PROCESSED,
    FRAUD_DETECTED,
    COMPLETED
}