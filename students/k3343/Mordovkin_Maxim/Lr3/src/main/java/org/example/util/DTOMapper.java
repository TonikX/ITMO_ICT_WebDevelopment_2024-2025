// src/main/java/org/example/util/DTOMapper.java

package org.example.util;

import org.example.dto.CrewMemberDTO;
import org.example.entities.CrewMember;

public class DTOMapper {
    public static CrewMemberDTO toCrewMemberDTO(CrewMember cm) {
        CrewMemberDTO dto = new CrewMemberDTO();
        dto.setCrewMemberId(cm.getCrewMemberId());
        dto.setFullName(cm.getFullName());
        dto.setAge(cm.getAge());
        dto.setEducation(cm.getEducation());
        dto.setWorkExperience(cm.getWorkExperience());
        dto.setPassportData(cm.getPassportData());
        dto.setPermissionType(cm.getPermissionType());
        dto.setEmploymentStatus(cm.getEmploymentStatus());
        dto.setRoleName(cm.getRoleName());
        dto.setFlightId(cm.getFlight() != null ? cm.getFlight().getFlightId() : null);
        dto.setUserId(cm.getUser() != null ? cm.getUser().getUserId() : null);
        dto.setCrewId(cm.getCrew() != null ? cm.getCrew().getCrewId() : null);
        return dto;
    }
}
