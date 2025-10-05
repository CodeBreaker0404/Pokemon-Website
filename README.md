# Pokemon-Website
This project enables us to view, sort and categorize all the pokemon data. There is also a feature to do team building in this.

The folder structure of this project is as follows-

backend-
    data-
      ->pokemon.csv
    ->add_forms.py
    ->app.py
    ->scrape_to_excel.py
    ->requirements.txt
frontend-
  assets-
    ->image_path.jpg
    ->intro_video.mp4
  ->index.html
  ->team.html


Now, I will try to explain the purpose of each file according to the priority-

backend/app.py->
->Load backend/data/pokemon.csv into memory with pandas.
->Normalize columns (parse stringified JSON lists for types / abilities).
->Compute/return a sprite URL for each Pokémon:
->Prefer sprite column (if provided).
->Fallback to a default PokeAPI sprite by id.

backend/scrape_to_excel.py->
->Data acquisition script to scrape Pokémon (name, id, types, abilities, region, optional form/slug and sprite) and write to backend/data/pokemon.csv.
->This should be run before the execution of the project. The purpose of this file is to create data.

  backend/add_forms.py
  ->It is to add variety of spriites which were missing in the scrape_to_excel.py. This should also be run before execution.

  backend/pokemon.csv->
  The data in it is-
  id- int
  name- string
  types- list
  abilities- list
  region- string
  slug- gets from external source.

  frontend/index.html->
  -> Hero with intro video
  ->Navbar-
      1. Search Bar
      2.Region- dropdown menu
      3.Type- dropdown menu
      4.Show all/Reset.
      5.Team builder button
    ->Lazy data load
    ->Render responsive card.
    ->Auto-scroll to results when we type in search or apply filters.

  frontend/team_builder.html->
  ->This is a seperate page which we can access from NavBar.
  ->Fetches /api/pokemon and fills a <datalist> (includes form names like “Raichu (Alolan)”).
  ->Export JSON downloads team.json with { "id": ..., "name": "..." }.

  frontend/assets->
    ->intro_video.mp4- has the video for hero class.
    ->image_path.jpg- transition from video into image with a glitch animation.

  backend/requirements.txt-
    -> run with the command-
      ```bash
      pip install -r backend/requirements.txt
      --force


Exection-

1. Create a virtual environment using the requirements.txt with the given command
   ```bash
   python -m venv venv
   --force

2. Run the backend/app.py file with
   ```bash
   python app.py

3. Open the frontend/index.html and Go into live server/view the page.


Running-

  

Update: README refined on 2025-10-05.
