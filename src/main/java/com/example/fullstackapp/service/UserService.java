package com.example.fullstackapp.service;

import com.example.fullstackapp.model.User;
import com.example.fullstackapp.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public List<User> getAllUsers(){
        return userRepository.findAll();
    }

    public Optional<User> getUserById(Long id){
        return userRepository.findById(id);
    }

    public User createUser(User user)
    {
        return userRepository.save(user);
    }

    public User updateUser(Long id, User userDetails)
    {
        User user = userRepository.findById(id).orElseThrow(()-> new RuntimeException("User not found."));
        user.setName(userDetails.getName());
        user.setEmail(userDetails.getEmail());
        return userRepository.save(user);
    }

    public void deleteUser(Long id)
    {
        userRepository.deleteById(id);
    }

    public User registerUser(User user) {
        if (userRepository.findByUserName(user.getUserName()).isPresent()) {
            throw new RuntimeException("Username already taken.");
        }
        // You can add password encryption here if needed
        return userRepository.save(user);
    }

    // ✅ Authenticate user during login
    public Optional<User> authenticateUser(String userName, String password) {
        return userRepository.findByUserName(userName)
                .filter(user -> user.getPassword().equals(password));
    }
    
}
