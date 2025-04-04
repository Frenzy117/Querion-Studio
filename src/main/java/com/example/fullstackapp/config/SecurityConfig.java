// package com.example.fullstackapp.config;

// import org.springframework.context.annotation.Bean;
// import org.springframework.context.annotation.Configuration;
// import org.springframework.security.config.annotation.web.builders.HttpSecurity;
// import org.springframework.security.web.SecurityFilterChain;

// @Configuration
// public class SecurityConfig {

//     @Bean
//     public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
//         http
//             .cors()
//             .and()
//             .csrf().disable() // Disable CSRF for testing (careful in production)
//             .authorizeHttpRequests(auth -> auth
//                 .requestMatchers("/api/auth/**").permitAll() // Allow auth routes without authentication
//                 .anyRequest().authenticated()
//             );

//         return http.build();
//     }
// }
