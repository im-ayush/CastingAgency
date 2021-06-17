import React from 'react';
import {
  BrowserRouter,
  Switch,
  Route
} from 'react-router-dom';

import App from './App';
import MovieList from './components/movies/MovieList.js';
import ActorList from './components/actors/ActorList.js';
import Movie from './components/movies/Movie.js';
import Actor from './components/actors/Actor.js';
import MovieAdd from './components/movies/MovieAdd.js';
import ActorAdd from './components/actors/ActorAdd.js';
import MovieUpdate from './components/movies/MovieUpdate.js';
import ActorUpdate from './components/actors/ActorUpdate.js';

const Routes = () => {
  return (
    <BrowserRouter>
      <Switch>
        <Route path="/" exact component={App} />
        <Route path="/movies" exact component={MovieList}/>
        <Route path="/actors" exact component={ActorList}/>
        <Route path="/movies/new" exact component={MovieAdd}/>
        <Route path="/actors/new" exact component={ActorAdd}/>
        <Route path="/movies/update/:id" exact component={MovieUpdate}/>
        <Route path="/actors/update/:id" exact component={ActorUpdate}/>
        <Route path="/movies/:id" exact component={Movie}/>
        <Route path="/actors/:id" exact component={Actor}/>
      </Switch>
    </BrowserRouter>
  );
};

export default Routes;
