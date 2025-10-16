package com.campuscoord.dao;

import com.campuscoord.model.Event;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Statement;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

@Repository
public class EventDao {

    private final JdbcTemplate jdbc;

    public EventDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<Event> findAll() {
        String sql = "SELECT id, title, description, organizer_id, start_time, end_time, venue, status, created_at FROM events";
        return jdbc.query(sql, (rs, rowNum) -> new Event(
                rs.getInt("id"),
                rs.getString("title"),
                rs.getString("description"),
                (Integer) rs.getObject("organizer_id"),
                toLocalDateTime(rs.getTimestamp("start_time")),
                toLocalDateTime(rs.getTimestamp("end_time")),
                rs.getString("venue"),
                rs.getString("status"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ));
    }

    public List<Event> findApproved() {
        String sql = "SELECT id, title, description, organizer_id, start_time, end_time, venue, status, created_at FROM events WHERE status = 'approved'";
        return jdbc.query(sql, (rs, rowNum) -> new Event(
                rs.getInt("id"),
                rs.getString("title"),
                rs.getString("description"),
                (Integer) rs.getObject("organizer_id"),
                toLocalDateTime(rs.getTimestamp("start_time")),
                toLocalDateTime(rs.getTimestamp("end_time")),
                rs.getString("venue"),
                rs.getString("status"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ));
    }

    public Event findById(int id) {
        String sql = "SELECT id, title, description, organizer_id, start_time, end_time, venue, status, created_at FROM events WHERE id = ?";
        return jdbc.queryForObject(sql, (rs, rowNum) -> new Event(
                rs.getInt("id"),
                rs.getString("title"),
                rs.getString("description"),
                (Integer) rs.getObject("organizer_id"),
                toLocalDateTime(rs.getTimestamp("start_time")),
                toLocalDateTime(rs.getTimestamp("end_time")),
                rs.getString("venue"),
                rs.getString("status"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ), id);
    }

    public int create(Event event) {
        String sql = "INSERT INTO events (title, description, organizer_id, start_time, end_time, venue, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            ps.setString(1, event.getTitle());
            ps.setString(2, event.getDescription());
            if (event.getOrganizerId() != null) ps.setObject(3, event.getOrganizerId()); else ps.setObject(3, null);
            ps.setTimestamp(4, toTimestamp(event.getStartTime()));
            ps.setTimestamp(5, toTimestamp(event.getEndTime()));
            ps.setString(6, event.getVenue());
            ps.setString(7, event.getStatus() != null ? event.getStatus() : "pending");
            ps.setTimestamp(8, toTimestamp(event.getCreatedAt()));
            return ps;
        }, keyHolder);

        Number key = keyHolder.getKey();
        return key != null ? key.intValue() : -1;
    }

    public void updateStatus(int eventId, String status) {
        String sql = "UPDATE events SET status = ? WHERE id = ?";
        jdbc.update(sql, status, eventId);
    }

    public void delete(int id) {
        String sql = "DELETE FROM events WHERE id = ?";
        jdbc.update(sql, id);
    }

    private static LocalDateTime toLocalDateTime(Timestamp ts) {
        return ts == null ? null : ts.toLocalDateTime();
    }

    private static Timestamp toTimestamp(LocalDateTime ldt) {
        return ldt == null ? null : Timestamp.valueOf(ldt);
    }
}
