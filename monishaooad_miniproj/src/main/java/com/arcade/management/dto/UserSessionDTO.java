package com.arcade.management.dto;

import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserSessionDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    private Integer id;
    private String username;
}
