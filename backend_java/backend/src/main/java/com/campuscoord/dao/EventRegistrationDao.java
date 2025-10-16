package com.campuscoord.dao;

import com.campuscoord.model.EventRegistration;
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
public class EventRegistrationDao {

    private final JdbcTemplate jdbc;

    public EventRegistrationDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public List<EventRegistration> findByUserId(int userId) {
        String sql = "SELECT id, event_id, user_id, registered_at, status FROM event_registrations WHERE user_id = ? AND status = 'active'";
        return jdbc.query(sql, (rs, rowNum) -> new EventRegistration(
                rs.getInt("id"),
                rs.getInt("event_id"),
                rs.getInt("user_id"),
                toLocalDateTime(rs.getTimestamp("registered_at")),
                rs.getString("status")
        ), userId);
    }

    public List<EventRegistration> findByEventId(int eventId) {
        String sql = "SELECT id, event_id, user_id, registered_at, status FROM event_registrations WHERE event_id = ? AND status = 'active'";
        return jdbc.query(sql, (rs, rowNum) -> new EventRegistration(
                rs.getInt("id"),
                rs.getInt("event_id"),
                rs.getInt("user_id"),
                toLocalDateTime(rs.getTimestamp("registered_at")),
                rs.getString("status")
        ), eventId);
    }

    public EventRegistration findByEventAndUser(int eventId, int userId) {
        String sql = "SELECT id, event_id, user_id, registered_at, status FROM event_registrations WHERE event_id = ? AND user_id = ?";
        List<EventRegistration> results = jdbc.query(sql, (rs, rowNum) -> new EventRegistration(
                rs.getInt("id"),
                rs.getInt("event_id"),
                rs.getInt("user_id"),
                toLocalDateTime(rs.getTimestamp("registered_at")),
                rs.getString("status")
        ), eventId, userId);
        return results.isEmpty() ? null : results.get(0);
    }

    public int create(EventRegistration registration) {
        String sql = "INSERT INTO event_registrations (event_id, user_id, registered_at, status) VALUES (?, ?, ?, ?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            ps.setInt(1, registration.getEventId());
            ps.setInt(2, registration.getUserId());
            ps.setTimestamp(3, toTimestamp(registration.getRegisteredAt()));
            ps.setString(4, registration.getStatus());
            return ps;
        }, keyHolder);

        Number key = keyHolder.getKey();
        return key != null ? key.intValue() : -1;
    }

    public void delete(int eventId, int userId) {
        String sql = "DELETE FROM event_registrations WHERE event_id = ? AND user_id = ?";
        jdbc.update(sql, eventId, userId);
    }

    public int countByEventId(int eventId) {
        String sql = "SELECT COUNT(*) FROM event_registrations WHERE event_id = ? AND status = 'active'";
        Integer count = jdbc.queryForObject(sql, Integer.class, eventId);
        return count != null ? count : 0;
    }

    private static LocalDateTime toLocalDateTime(Timestamp ts) {
        return ts == null ? null : ts.toLocalDateTime();
    }

    private static Timestamp toTimestamp(LocalDateTime ldt) {
        return ldt == null ? null : Timestamp.valueOf(ldt);
    }
}
