package com.polyglot.orderservice.application;

import com.polyglot.orderservice.domain.model.Order;
import com.polyglot.orderservice.domain.model.OrderRepository;
import com.polyglot.orderservice.domain.events.OrderCreatedEvent;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.cloud.stream.function.StreamBridge;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository repository;
    private final StreamBridge streamBridge;

    @Transactional
    public Order createOrder(OrderRequest request) {
        Order order = Order.builder()
                .customerEmail(request.customerEmail())
                .totalAmount(request.amount())
                .build();
        
        order = repository.save(order);
        
        streamBridge.send("orderCreated-out-0", 
            new OrderCreatedEvent(order.getId(), order.getCustomerEmail(), order.getTotalAmount(), LocalDateTime.now()));
            
        return order;
    }
}