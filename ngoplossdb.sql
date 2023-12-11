-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 10 Des 2023 pada 08.45
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
-- Database: `ngoplossdb`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `cafe`
--

CREATE TABLE `cafe` (
  `id` int(11) NOT NULL,
  `foto` varchar(225) DEFAULT NULL,
  `nama` varchar(225) DEFAULT NULL,
  `Link_gmaps` varchar(225) DEFAULT NULL,
  `deskripsi` text DEFAULT NULL,
  `jam_buka` varchar(225) DEFAULT NULL,
  `jam_tutup` varchar(225) DEFAULT NULL,
  `status` varchar(225) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nama_lokasi` varchar(225) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `cafe`
--

INSERT INTO `cafe` (`id`, `foto`, `nama`, `Link_gmaps`, `deskripsi`, `jam_buka`, `jam_tutup`, `status`, `user_id`, `nama_lokasi`) VALUES
(1, 'Market_Ifa.jpeg', 'r', 'r', 'r', '00:00:00', '00:00:00', 'rr', NULL, 'r'),
(3, '278470ef-09c8-4a09-ab78-ec847a474393.jpeg', 'tolrenasi', 'a', '10.00', '15.00', 'Buka', 'jalan turusna', NULL, 'a'),
(7, 'ahahhaha', 'WARMINDO AZIZ', 'LALALALLA', 'LALALALALALALA', '65', '77', NULL, NULL, 'mindo war');

-- --------------------------------------------------------

--
-- Struktur dari tabel `images`
--

CREATE TABLE `images` (
  `id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data untuk tabel `images`
--

INSERT INTO `images` (`id`, `file_name`) VALUES
(1, 'Camiseta_Oversized_Azul_Claro.jpeg');

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
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('pemilik_cafe','pengguna','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'arus', '231cfa1afc39564790c4e05404fb76f71a789b3c0433d35d3a94ad55a8d47909', 'pengguna'),
(2, 'ar', '1ea23a747abaaa6d026239d7d066791284db5babed8ab67ee6720f9cd072f67c', 'pengguna'),
(3, 'ikbal', '7ed2c74e9924575fccda0a9584833b32b1ed97a828aa621e99eb2b9e39c4222c', 'pemilik_cafe'),
(4, 'nana', '721aaf35bf450c0591679734483a4a3967afe03dfb720c8c67ffc0753c161cce', 'pengguna'),
(5, 'aku', '7ed2c74e9924575fccda0a9584833b32b1ed97a828aa621e99eb2b9e39c4222c', 'pemilik_cafe'),
(6, 'lala', '7ed2c74e9924575fccda0a9584833b32b1ed97a828aa621e99eb2b9e39c4222c', 'pengguna'),
(7, 'ala', '7ed2c74e9924575fccda0a9584833b32b1ed97a828aa621e99eb2b9e39c4222c', 'pemilik_cafe'),
(8, 'ala', 'ikbal123', 'pemilik_cafe'),
(9, 'asar', 'asar123', 'pemilik_cafe'),
(10, 'aryuss', 'aryus123', 'pengguna'),
(11, 'nanda', 'nandaboboho', 'pemilik_cafe');

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
-- Indeks untuk tabel `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cafe_id` (`cafe_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT untuk tabel `images`
--
ALTER TABLE `images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `cafe`
--
ALTER TABLE `cafe`
  ADD CONSTRAINT `cafe_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Ketidakleluasaan untuk tabel `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`cafe_id`) REFERENCES `cafe` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
