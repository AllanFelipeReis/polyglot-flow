package com.polyglot.orderservice.infrastructure.rest;

// Importe do pacote application (onde está seu Service e o Request)
import com.polyglot.orderservice.application.OrderService;
import com.polyglot.orderservice.application.OrderRequest; 

// Importe do pacote domain.model (onde está sua Entity)
import com.polyglot.orderservice.domain.model.Order;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    public ResponseEntity<Order> create(@RequestBody OrderRequest request) {
        // Chamando o método createOrder que você já tem pronto
        Order order = orderService.createOrder(request);
        return ResponseEntity.ok(order);
    }
}