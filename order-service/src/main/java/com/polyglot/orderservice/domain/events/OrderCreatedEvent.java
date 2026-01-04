package com.polyglot.orderservice.domain.events;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public record OrderCreatedEvent(
    Long orderId,
    String customerEmail,
    BigDecimal amount,
    LocalDateTime createdAt
) {}