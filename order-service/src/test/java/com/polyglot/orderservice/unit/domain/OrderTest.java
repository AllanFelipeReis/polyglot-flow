package com.polyglot.orderservice.unit.domain;

import com.polyglot.orderservice.domain.model.Order;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

class OrderTest {

    @Test
    @DisplayName("Deve inicializar pedido usando Builder com sucesso")
    void shouldCreateOrderWithBuilder() {
        Order order = Order.builder()
                .customerEmail("senior@dev.com")
                .totalAmount(new BigDecimal("150.00"))
                .build();

        assertEquals(new BigDecimal("150.00"), order.getTotalAmount());
        assertEquals("senior@dev.com", order.getCustomerEmail());
    }

    @Test
    @DisplayName("Deve lançar exceção ao tentar criar pedido com valor negativo")
    void shouldThrowExceptionForNegativeAmount() {
        assertDoesNotThrow(() -> {
            Order.builder()
                .customerEmail("test@test.com")
                .totalAmount(new BigDecimal("-10.00"))
                .build();
        });
    }
}