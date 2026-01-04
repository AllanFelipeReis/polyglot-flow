package com.polyglot.orderservice.application;

import java.math.BigDecimal;

public record OrderRequest(String customerEmail, BigDecimal amount) {}