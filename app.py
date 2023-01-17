from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3



app = Flask (__name__)


@app.route('/')
def index():
    db=sqlite3.connect('sid.db')
    cur=db.cursor()
    cur.execute("SELECT * FROM sppt")
    pbb=cur.fetchall()
    return render_template("index.html", pbb=pbb)


@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/tambah', methods=['GET','POST'])
def tambah():
   
    if request.method == 'POST':
        kelas = request.form['kelas']
        blok = request.form['blok']
        no = request.form['no']
        nop = request.form['nop']
        wp = request.form['wp']
        nik = request.form['nik']
               
        db=sqlite3.connect('sid.db')
        cur=db.cursor()
        cur.execute("INSERT INTO sppt(kelas,blok,no,nop,wp,nik) VALUES('"+kelas+"','"+blok+"','"+no+"','"+nop+"','"+wp+"','"+nik+"') ")
        db.commit()

        return redirect(url_for('index'))
    return render_template("tables.html")


@app.route('/editsppt/<string:nop>', methods=['GET','POST'])
def editsppt(nop):
    db=sqlite3.connect('sid.db')
    cur=db.cursor()
    cur.execute("SELECT * FROM sppt where nop=?",(nop,))
    sppt=cur.fetchone()
    return render_template("editsppt.html", sppt=sppt)
    if request.method=='POST':
        kelas = request.form['kelas']
        blok = request.form['blok']
        no = request.form['no']
        nop = request.form['nop']
        wp = request.form['wp']
        nik = request.form['nik']
        db=sqlite3.connect('sid.db')
        cur=db.cursor()
        cur.execute("UPDATE sppt SET kelas=?, blok=?, no=?, nop=?, wp=?, nik=? WHERE nop=?", (kelas,blok,no,nop,wp,nik,nop))
        db.commit()
        return redirect(url_for('index'))
    return render_template('editsppt.html', sppt=sppt)

@app.route('/lihatop/<string:nik>')
def lihatop(nik):
    db=sqlite3.connect('sid.db')
    cur=db.cursor()
    cur.execute("SELECT * FROM penduduk where nik=?",(nik,))
    data=cur.fetchone()
    cur.execute("SELECT COUNT (*) FROM sppt where nik=?",(nik,))
    jumlah = str(cur.fetchone()[0])
    
    cur.execute("SELECT * FROM sppt where nik=?",(nik,))
    namapbb=cur.fetchall()
    return render_template("lihatop.html", pbb=namapbb, data=data, jumlah=jumlah)


@app.route('/lihat/<string:wp>')
def lihat(wp):
    
    return render_template("map.html")


@app.route('/penduduk')
def penduduk():
	db=sqlite3.connect('sid.db')
	cur=db.cursor()
	cur.execute("SELECT * FROM p3ke INNER JOIN dtks WHERE p3ke.field3=dtks.field4")
	jmlpenduduk=cur.fetchall()
	return render_template('bootstrap_table.html',jmlpenduduk=jmlpenduduk)

@app.route('/dhkp')
def dhkp():
	db=sqlite3.connect('sid.db')
	cur=db.cursor()
	cur.execute("SELECT * FROM dhkp2019 INNER JOIN sppt WHERE dhkp2019.nop=sppt.nop")
	datanya=cur.fetchall()
	return render_template('dhkp.html',datanya=datanya)


@app.route('/hapus/<string:nik>',methods=['GET'])
def hapus(nik):
    db=sqlite3.connect('sid.db')
    cur=db.cursor()
    cur.execute("DELETE FROM sppt WHERE nik=?",(nik,))
    db.commit()
    flash('Data terhapus','warning')
    return redirect(url_for("index"))

    
app.secret_key = '\xf9@8\xb3\x83\xb5\x02\x1c\xd6p4\x14\x1f93\xa2\x83\xa7\xaf#\x84\xacv\x91'
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
