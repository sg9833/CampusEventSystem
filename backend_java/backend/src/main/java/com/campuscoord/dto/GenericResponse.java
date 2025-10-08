package com.campuscoord.dto;

import java.util.Map;

public class GenericResponse {

    private boolean success;
    private String message;
    private Map<String, Object> data;

    public GenericResponse() {}

    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }

    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }

    public Map<String, Object> getData() { return data; }
    public void setData(Map<String, Object> data) { this.data = data; }
}
