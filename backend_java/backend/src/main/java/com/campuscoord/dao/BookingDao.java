package com.campuscoord.dao;

import com.campuscoord.model.Booking;
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
public class BookingDao {

    private final JdbcTemplate jdbc;

    public BookingDao(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public int countConflicts(int resourceId, Timestamp start, Timestamp end) {
        String sql = "SELECT COUNT(*) FROM bookings WHERE resource_id = ? AND NOT (end_time <= ? OR start_time >= ?)";
        Integer count = jdbc.queryForObject(sql, Integer.class, resourceId, start, end);
        return count == null ? 0 : count;
    }

    public int createBooking(Booking booking) {
        String sql = "INSERT INTO bookings (event_id, user_id, resource_id, start_time, end_time, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            if (booking.getEventId() != null) ps.setObject(1, booking.getEventId()); else ps.setObject(1, null);
            ps.setInt(2, booking.getUserId());
            ps.setInt(3, booking.getResourceId());
            ps.setTimestamp(4, toTimestamp(booking.getStartTime()));
            ps.setTimestamp(5, toTimestamp(booking.getEndTime()));
            ps.setString(6, booking.getStatus());
            ps.setTimestamp(7, toTimestamp(booking.getCreatedAt()));
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

    private static Timestamp toTimestamp(LocalDateTime ldt) {
        return ldt == null ? null : Timestamp.valueOf(ldt);
    }
}
