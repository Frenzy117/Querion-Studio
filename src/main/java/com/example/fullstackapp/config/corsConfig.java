// package com.example.fullstackapp.config;
// import org.springframework.context.annotation.Bean;
// import org.springframework.context.annotation.Configuration;
// import org.springframework.web.cors.CorsConfiguration;
// import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
// import org.springframework.web.filter.CorsFilter;

// import java.util.List;
// import java.util.logging.Logger;

// @Configuration
// public class corsConfig {

//     private static final Logger LOGGER = Logger.getLogger(corsConfig.class.getName());

//     @Bean
//     public CorsFilter corsFilter() {
//         CorsConfiguration config = new CorsConfiguration();
//         config.setAllowCredentials(true);
//         config.setAllowedOrigins(List.of("http://localhost:3000")); 
//         config.setAllowedHeaders(List.of("Authorization", "Content-Type", "Accept", "X-Requested-With"));
//         config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS")); 

//         LOGGER.info("CORS configuration loaded");

//         UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
//         source.registerCorsConfiguration("/**", config);
//         return new CorsFilter(source);
//     }
// }
