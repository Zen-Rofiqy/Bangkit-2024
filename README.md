# Bangkit Academy 2024
  
# Refleksi diri
### Sasaran Pengembangan Skill
Siswa mampu menceritakan kembali dan melaporkan hal yang didapatkan selama proses pembelajaran dalam bentuk lisan dan tulisan.  

## Detil Pembelajaran
Siswa mengisi logbook, memberikan laporan ke dosen pembimbing akademik, serta refleksi pembelajaran secara mandiri.  
+ 3 jam per minggu
  
## Metode Asesmen
Penilaian dilakukan berdasarkan ketepatan waktu pengisian logbook dan feedback yang diberikan oleh dosen pembimbing akademik.

### Git Bash Notes
Just select all and copy the sytnax/command
> EZ Normal Push/Upload
```bash
git pull origin HEAD:main
git add . --all
git commit -m "Update"
git push origin HEAD:main 
```

> EZ Push Large Files (More than 100mb)  
Just change the large file extention.   
For this case, my large file is `.csv`
```bash
git lfs install 
git lfs track "*.csv"
git add . --all
git commit -m "Update"
git lfs migrate import --include="*.csv"
git push origin HEAD:main 
```
