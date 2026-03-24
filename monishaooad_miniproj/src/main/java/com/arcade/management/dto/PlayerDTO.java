package com.arcade.management.dto;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;
@Data
public class PlayerDTO {
    @NotBlank(message = "Username is required") @Size(min = 3, max = 50)
    private String username;
    @NotBlank(message = "Email is required") @Email(message = "Invalid email format")
    private String email;
    private String avatar;
}