//package ru.barkhatnat.cinema.exception;
//
//import org.springframework.http.HttpStatus;
//import org.springframework.http.ProblemDetail;
//import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.ControllerAdvice;
//import org.springframework.web.bind.annotation.ExceptionHandler;
//
//@ControllerAdvice
//public class ForbiddenControllerAdvice {
//    @ExceptionHandler(ForbiddenException.class)
//    public ResponseEntity<ProblemDetail> handleForbiddenException(ForbiddenException e) {
//        ProblemDetail problemDetail = ProblemDetail.forStatusAndDetail(HttpStatus.FORBIDDEN, e.getMessage());
//        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(problemDetail);
//    }
//}