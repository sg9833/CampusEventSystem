package com.campuscoord.service;

import com.campuscoord.model.Booking;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.sql.PreparedStatement;
import java.sql.Statement;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class BookingService {

    private final JdbcTemplate jdbc;

    public BookingService(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @Transactional
    public int createBooking(int userId, int resourceId, LocalDateTime start, LocalDateTime end, Integer eventId) {
        String conflictSql = "SELECT COUNT(*) FROM bookings WHERE resource_id = ? AND status = 'CONFIRMED' AND NOT (end_time <= ? OR start_time >= ?)";
        Timestamp startTs = Timestamp.valueOf(start);
        Timestamp endTs = Timestamp.valueOf(end);
        Integer conflicts = jdbc.queryForObject(conflictSql, Integer.class, resourceId, startTs, endTs);
        if (conflicts != null && conflicts > 0) {
            throw new IllegalStateException("Resource already booked for requested time range");
        }

        String insertSql = "INSERT INTO bookings (event_id, user_id, resource_id, start_time, end_time, status, created_at) VALUES (?, ?, ?, ?, ?, 'CONFIRMED', NOW())";
        KeyHolder keyHolder = new GeneratedKeyHolder();

        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(insertSql, Statement.RETURN_GENERATED_KEYS);
            if (eventId != null) ps.setObject(1, eventId); else ps.setObject(1, null);
            ps.setInt(2, userId);
            ps.setInt(3, resourceId);
            ps.setTimestamp(4, startTs);
            ps.setTimestamp(5, endTs);
            return ps;
        }, keyHolder);

        Number key = keyHolder.getKey();
        return key != null ? key.intValue() : -1;
    }

    public List<Booking> listBookingsForUser(int userId) {
        String sql = "SELECT id, event_id, user_id, resource_id, start_time, end_time, status, created_at FROM bookings WHERE user_id = ? ORDER BY start_time";
        return jdbc.query(sql, (rs, rowNum) -> new Booking(
                rs.getInt("id"),
                (Integer) rs.getObject("event_id"),
                rs.getInt("user_id"),
                rs.getInt("resource_id"),
                toLocalDateTime(rs.getTimestamp("start_time")),
                toLocalDateTime(rs.getTimestamp("end_time")),
                rs.getString("status"),
                toLocalDateTime(rs.getTimestamp("created_at"))
        ), userId);
    }

    private static LocalDateTime toLocalDateTime(Timestamp ts) {
        return ts == null ? null : ts.toLocalDateTime();
    }
}
