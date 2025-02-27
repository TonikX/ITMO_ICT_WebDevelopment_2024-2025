// src/main/java/org/example/dto/CrewMemberDTO.java

package org.example.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CrewMemberDTO {
    private Long crewMemberId;
    private String fullName;
    private Integer age;
    private String education;
    private Integer workExperience;
    private String passportData;
    private String permissionType;
    private String roleName;
    private String employmentStatus;
    private Long flightId;
    private Long userId;
    private Long crewId;

}
