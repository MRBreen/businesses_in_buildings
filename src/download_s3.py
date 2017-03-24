import boto3
import botocore


if __name__ == '__main__':
  s3 = boto3.resource('s3')
  b = s3.Bucket('biz-in-buildings-stage')

  filenames = [key.key for key in b.objects.all()]
  #filenames = [b.key.encode('utf-8') for b in bo.iterator()]

  print "files to download:" , filenames
  #for file in os.listdir('../data/'):  #for local

  for key in b.objects.all():
      extracted = extract()
      extracted.build(key)
      #if db.biz.find( { "Filename" : key.key} ).count() < 1:
      write_to_s3(details, filename)
      print "downloading file from S3:" , collection.count()
