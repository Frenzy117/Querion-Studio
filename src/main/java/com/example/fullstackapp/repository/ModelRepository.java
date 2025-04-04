package com.example.fullstackapp.repository;

import com.example.fullstackapp.model.AIModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ModelRepository extends JpaRepository<AIModel,Long>{
    Optional<AIModel> findByName(String name);
    
} 
