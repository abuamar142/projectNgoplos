-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 07 Des 2023 pada 21.33
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ngoplosdb`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `cafe`
--

CREATE TABLE `cafe` (
  `id` int(11) NOT NULL,
  `nama` varchar(225) DEFAULT NULL,
  `Link_gmaps` varchar(225) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `jam_buka` time DEFAULT NULL,
  `jam_tutup` time DEFAULT NULL,
  `status` varchar(225) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `cafe_fasilitas`
--

CREATE TABLE `cafe_fasilitas` (
  `cafe_id` int(11) DEFAULT NULL,
  `Fasilitas_id` int(11) DEFAULT NULL,
  `Keterangan` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `cafe_rating`
--

CREATE TABLE `cafe_rating` (
  `cafe_id` int(11) DEFAULT NULL,
  `rating_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `fasilitas`
--

CREATE TABLE `fasilitas` (
  `id` int(11) NOT NULL,
  `Wifi` tinyint(1) DEFAULT NULL,
  `Tempat_merokok` tinyint(1) DEFAULT NULL,
  `Stopkontak` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `Kategori` enum('makanan','minuman') DEFAULT NULL,
  `Nama` varchar(225) DEFAULT NULL,
  `Harga` int(11) DEFAULT NULL,
  `cafe_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `rating`
--

CREATE TABLE `rating` (
  `id` int(11) NOT NULL,
  `Rating` varchar(225) DEFAULT NULL,
  `Komentar` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('pemilik_cafe','pengguna','','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'la ode arus hidayat', 'Asasdada10', 'pengguna'),
(2, 'la ode arus hidayat', 'Asasdada10', 'pengguna'),
(3, 'dayat', 'dayat123', 'pemilik_cafe'),
(4, 'kabil', 'kabil123', 'pemilik_cafe'),
(5, 'arus', 'kabil123', 'pengguna'),
(6, 'arus', 'Asasdada10', 'pemilik_cafe'),
(7, 'arus', 'Asasdada10', 'pemilik_cafe'),
(8, 'ahmad', 'kabil123', 'pengguna'),
(9, 'ahmad', 'kabil123', 'pengguna'),
(10, 'arus', 'Asasdada10', 'pemilik_cafe'),
(11, 'ikbal', '7ed2c74e9924575fccda0a9584833b32b1ed97a828aa621e99eb2b9e39c4222c', 'pemilik_cafe'),
(12, 'amu', '5484a8be8bcc8e37bbb37f427c2ebfe693a8c856e7fa63ae81af692b89a61ca6', 'pengguna'),
(13, 'amu', '5484a8be8bcc8e37bbb37f427c2ebfe693a8c856e7fa63ae81af692b89a61ca6', 'pengguna'),
(14, 'amu', '92580bc01ec323d7d216b549912185d89af5c19d87983c515e0c6beef422e149', 'pengguna'),
(15, 'amu', 'e11e4c7323169fe7087c4e0266e36c61fae289b8284504390028f20b87972de2', 'pengguna'),
(16, 'la ode arus hidayar', 'e11e4c7323169fe7087c4e0266e36c61fae289b8284504390028f20b87972de2', 'pengguna');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `cafe`
--
ALTER TABLE `cafe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `cafe_fasilitas`
--
ALTER TABLE `cafe_fasilitas`
  ADD KEY `cafe_id` (`cafe_id`),
  ADD KEY `Fasilitas_id` (`Fasilitas_id`);

--
-- Indeks untuk tabel `cafe_rating`
--
ALTER TABLE `cafe_rating`
  ADD KEY `cafe_id` (`cafe_id`),
  ADD KEY `rating_id` (`rating_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `fasilitas`
--
ALTER TABLE `fasilitas`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cafe_id` (`cafe_id`);

--
-- Indeks untuk tabel `rating`
--
ALTER TABLE `rating`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `cafe`
--
ALTER TABLE `cafe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `fasilitas`
--
ALTER TABLE `fasilitas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `rating`
--
ALTER TABLE `rating`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `cafe`
--
ALTER TABLE `cafe`
  ADD CONSTRAINT `cafe_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ketidakleluasaan untuk tabel `cafe_fasilitas`
--
ALTER TABLE `cafe_fasilitas`
  ADD CONSTRAINT `cafe_fasilitas_ibfk_1` FOREIGN KEY (`cafe_id`) REFERENCES `cafe` (`id`),
  ADD CONSTRAINT `cafe_fasilitas_ibfk_2` FOREIGN KEY (`Fasilitas_id`) REFERENCES `fasilitas` (`id`);

--
-- Ketidakleluasaan untuk tabel `cafe_rating`
--
ALTER TABLE `cafe_rating`
  ADD CONSTRAINT `cafe_rating_ibfk_1` FOREIGN KEY (`cafe_id`) REFERENCES `cafe` (`id`),
  ADD CONSTRAINT `cafe_rating_ibfk_2` FOREIGN KEY (`rating_id`) REFERENCES `rating` (`id`),
  ADD CONSTRAINT `cafe_rating_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ketidakleluasaan untuk tabel `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`cafe_id`) REFERENCES `cafe` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
