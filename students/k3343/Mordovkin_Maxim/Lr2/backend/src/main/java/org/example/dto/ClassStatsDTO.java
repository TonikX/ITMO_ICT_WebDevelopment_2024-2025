package org.example.dto;

import java.io.Serializable;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ClassStatsDTO implements Serializable {
    private Long assignmentId;
    private String title;
    private Double avgGrade;

    public ClassStatsDTO() {}

    public ClassStatsDTO(Long assignmentId, String title, Double avgGrade) {
        this.assignmentId = assignmentId;
        this.title = title;
        this.avgGrade = avgGrade;
    }
}
