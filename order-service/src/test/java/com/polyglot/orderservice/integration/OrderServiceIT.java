package com.polyglot.orderservice.integration;

import com.polyglot.orderservice.application.OrderService;
import com.polyglot.orderservice.application.OrderRequest;
import com.polyglot.orderservice.domain.model.Order;
import com.polyglot.orderservice.domain.model.OrderRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.containers.RabbitMQContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

@SpringBootTest
@Testcontainers
class OrderServiceIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15-alpine");
    
    @Container
    static RabbitMQContainer rabbit = new RabbitMQContainer("rabbitmq:3-management-alpine");

    @Autowired
    private OrderService orderService;

    @Autowired
    private OrderRepository repository;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.rabbitmq.host", rabbit::getHost);
        registry.add("spring.rabbitmq.port", rabbit::getAmqpPort);
    }

    @Test
    @DisplayName("Deve salvar pedido no banco e disparar evento para o broker")
    void shouldCreateOrderAndPublishEvent() {
        // Arrange
        OrderRequest request = new OrderRequest("dev@senior.com", new BigDecimal("99.90"));

        // Act
        Order savedOrder = orderService.createOrder(request);

        // Assert
        assertNotNull(savedOrder.getId());
        assertEquals(1, repository.count());
    }
}