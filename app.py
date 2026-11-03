                st.error("The video has invalid frame dimensions.")
                st.stop()

            zone = (
                int(width * zone_left / 100),
                int(height * zone_top / 100),
                int(width * zone_right / 100),
                int(height * zone_bottom / 100),
            )

            writer = cv2.VideoWriter(
                str(output_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (width, height),
            )
            if not writer.isOpened():
                st.error("Could not create the annotated video on this system.")
                cap.release()
                st.stop()

            try:
                model = load_model()
            except Exception as exc:
                cap.release()
                writer.release()
                st.error(f"Could not load YOLO model: {exc}")
                st.stop()

            event_log = []
            intrusion_frames = 0
            frame_number = 0
            progress = st.progress(0)
            status = st.empty()

            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                frame_number += 1

                cv2.rectangle(frame, (zone[0], zone[1]), (zone[2], zone[3]), (0, 165, 255), 2)
                cv2.putText(
                    frame, "RESTRICTED ZONE", (zone[0], max(25, zone[1] - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 165, 255), 2
                )

                results = model.predict(frame, conf=confidence, classes=[0], verbose=False)
                frame_has_intrusion = False

                for result in results:
                    if result.boxes is None:
                        continue
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        center_x = (x1 + x2) // 2
                        center_y = (y1 + y2) // 2
                        inside = point_in_rect(center_x, center_y, zone)
                        color = (0, 0, 255) if inside else (0, 200, 0)
                        label = "PERSON — ZONE ALERT" if inside else "PERSON"
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.circle(frame, (center_x, center_y), 4, color, -1)
                        cv2.putText(
                            frame, label, (x1, max(20, y1 - 8)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
                        )
                        if inside:
                            frame_has_intrusion = True

                if frame_has_intrusion:
                    intrusion_frames += 1
                    event_log.append({
                        "frame": frame_number,
                        "timestamp_seconds": round(frame_number / fps, 3),
                        "event": "person_detected_inside_demo_zone",
                    })

                cv2.putText(
                    frame, f"Frame: {frame_number} | Alert frames: {intrusion_frames}",
                    (12, height - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
                )
                writer.write(frame)

                if total_frames > 0:
                    progress.progress(min(frame_number / total_frames, 1.0))
                status.write(f"Processed {frame_number} frames...")

            cap.release()
            writer.release()

            output_bytes = output_path.read_bytes() if output_path.exists() else b""
            output_hash = hashlib.sha256(output_bytes).hexdigest() if output_bytes else ""
            report = {
                "project": "IBVAP",
                "input_file": uploaded.name,
                "input_sha256": sha256,
                "processed_frames": frame_number,
                "alert_frames": intrusion_frames,
                "events": event_log,
                "output_sha256": output_hash,
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "note": "Prototype output; detections require human review.",
            }

            status.success("Video analysis completed.")
            col1, col2 = st.columns(2)
            col1.metric("Frames processed", frame_number)
            col2.metric("Frames with zone alerts", intrusion_frames)

            if output_bytes:
                st.subheader("Annotated video")
                st.video(output_bytes)
                st.download_button(
                    "Download annotated video",
                    data=output_bytes,
                    file_name="ibvap_annotated.mp4",
                    mime="video/mp4",
                )

            st.subheader("Evidence report")
            st.json(report)
            st.download_button(
                "Download event report (JSON)",
                data=json.dumps(report, indent=2),
                file_name="ibvap_event_report.json",
                mime="application/json",
            )
else:
