package com.campuscoord.dao;

import com.campuscoord.model.Resource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public class ResourceDao {

    private final JdbcTemplate jdbc;

    public ResourceDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Resource> findAll() {
        String sql = "SELECT id, name, type, capacity, location, is_active, created_at FROM resources";
        return jdbc.query(sql, (rs, rowNum) -> new Resource(
                rs.getInt("id"),
                rs.getString("name"),
                rs.getString("type"),
                (Integer) rs.getObject("capacity"),
                rs.getString("location"),
                rs.getBoolean("is_active"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ));
    }

    public Resource findById(int id) {
        String sql = "SELECT id, name, type, capacity, location, is_active, created_at FROM resources WHERE id = ?";
        return jdbc.queryForObject(sql, (rs, rowNum) -> new Resource(
                rs.getInt("id"),
                rs.getString("name"),
                rs.getString("type"),
                (Integer) rs.getObject("capacity"),
                rs.getString("location"),
                rs.getBoolean("is_active"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ), id);
    }

    private static LocalDateTime toLocalDateTime(Timestamp ts) {
        return ts == null ? null : ts.toLocalDateTime();
    }
}
