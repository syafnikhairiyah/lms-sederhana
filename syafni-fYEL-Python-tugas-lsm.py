print("""
*******************************
*                             *
** LIBRARY MANAGEMENT SYSTEM **   
*                             *
*******************************
1. Pendaftaran User Baru
2. Pendaftaran Buku Baru
3. Peminjaman
4. Tampilkan Daftar Buku
5. Tampilkan Daftar User
6. Tampilkan Daftar Peminjaman
7. Cari Buku
8. Pengembalian
9. Exit
\n""")

import datetime
import mysql.connector as con
from tabulate import tabulate
import creds

# edit creds.py to match your db settings
db = con.connect(host = creds.host, user = creds.user, password = creds.password, database = creds.database)
cursor = db.cursor()

#starting main loop
status = True
while status:
    choice = int(input("""Masukkan Nomor Tugas: """))

    # input user
    if choice == 1:
        member_name = str(input("Masukkan Nama User: "))
        contact = int(input("Masukkan No. Kontak User: "))
        #pekerjaan = str(input("Masukkan Pekerjaan User: "))
        #alamat = str(input("Masukkan Alamat User: "))
        sql = "insert into members values(NULL,%s,%s)"
        val = (member_name, contact)
        cursor.execute(sql, val)
        if cursor.rowcount == 1:
            print("Input User Baru Berhasil\n")
            cursor.execute("commit")
        else:
            print("Error!")
            status = False
            break
        continue
        
    # input books
    if choice == 2:
        book_name = str(input("Masukkan Nama Buku: "))
        genre = str(input("Masukkan Kategori Buku: "))
        author = str(input("Masukkan Penulis Buku: "))
        sql = "insert into books values(NULL,%s,%s,%s)"
        val = (book_name, genre, author)
        cursor.execute(sql, val)
        db.commit()
        if cursor.rowcount == 1:
            print("Input Buku Baru Berhasil\n")
            cursor.execute("commit")
        else:
            print("Error!")
            status = False
            break
        continue
    
    #Peminjaman
    if choice == 3:
        # print all books
        print("List of all book IDs")
        cursor.execute("select book_id, name from books")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['Kode Buku','Judul','Kategori','Penulis'], tablefmt='psql'))
        book = int(input("Masukkan Book ID\n"))
                
        # print all members
        print("\nList of all member IDs")
        cursor.execute("select member_id, name from members")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['ID User','Nama','Kontak'], tablefmt='psql'))
        member = int(input("Masukkan User ID\n"))
                
        # issue a book
        sql = "insert into booking values(NULL,%s,%s, curdate(), NULL)"
        val = (member, book)
        cursor.execute(sql, val)
        if cursor.rowcount == 1:
            print("Transaksi Berhasil.\n")
            cursor.execute("commit")
        else:
            print("Error!")
            status = False
            break
        continue


    #books available
    if choice == 4:
        cursor.execute("select * from books")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['Kode Buku','Judul','Kategori','Penulis'], tablefmt='psql'))
        continue
    
    # all users
    if choice == 5:
        cursor.execute("select * from members")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['ID User','Nama','Kontak'], tablefmt='psql'))
        continue
    
    # Daftar peminjaman
    if choice == 6:
        cursor.execute("SELECT booking.order_id, members.name as Member, books.name as Book, booking.issue_date FROM booking join members ON booking.member_id = members.member_id join books ON booking.book_id = books.book_id")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['Order id','Nama User','Buku','Issue Date'], tablefmt='psql'))
        continue
    
    # Pencarian buku
    if choice == 7:
        keyword = str(input("Masukkan Kata Kunci Nama Buku: "))
        cursor.execute("select books.book_id, books.name, books.genre, books.author from books where books.name = %s", (keyword,))
        rows = cursor.fetchall()
        print(tabulate(rows, tablefmt='psql'))
        continue
    
    # Kembalikan Buku
    if choice == 8:
        # printing due records
        cursor.execute("SELECT booking.order_id, members.name as Member, books.name as Book, booking.issue_date FROM booking join members ON booking.member_id = members.member_id join books ON booking.book_id = books.book_id where booking.return_date is null")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=['Order id','Nama User','Buku','Issue Date'], tablefmt='psql'))
                
        # select booking id for returning book
        order = int(input("Masukkan Order ID\n"))

        # return a book
        sql = "update booking set return_date = curdate() where order_id = " + str(order)
        cursor.execute(sql)
        if cursor.rowcount > 0:
            print("Order id: %s closed succesfully.\n" %order)
            cursor.execute("commit")
        else:
            print("Error!")
        continue
        
    # Exit
    if choice == 9:
        print("*** Exiting Program ***")
        status = False

# close the connection
db.close()