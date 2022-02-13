zip: icefinder.zip
	zip -r icefinder.zip icons/ icefinder.js manifest.json

.PHONY: clean
clean:
	rm icefinder.zip
