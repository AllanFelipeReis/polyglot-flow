package com.polyglot.orderservice.infrastructure.rest;

import com.polyglot.orderservice.application.OrderService;
import com.polyglot.orderservice.application.OrderRequest; 

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
        Order order = orderService.createOrder(request);
        return ResponseEntity.ok(order);
    }
}